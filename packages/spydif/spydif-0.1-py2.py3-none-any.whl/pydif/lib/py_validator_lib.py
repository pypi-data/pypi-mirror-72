import os
import pypyodbc
import datetime
from decimal import *
import pandas as pd
import numpy as np
import logging
from configparser import ConfigParser
import os.path as path
from sqlalchemy import event
import sqlalchemy
import urllib
import shutil
from pydif.exception import customExceptions as ce
import sys
from pydif.lib.create_directory import make_folder

config = ConfigParser()
myConfigFileOSPath = path.join(path.dirname(path.dirname(__file__)), 'config', 'py_validator_config.cfg')
# print(myConfigFileOSPath)
config.read(myConfigFileOSPath)

_LogDir            = config.get('DIRECTORY', 'LOG_DIR')
_SourceDir         = config.get('DIRECTORY', 'SOURCE_DIR')
_TargetDir         = config.get('DIRECTORY', 'TARGET_DIR')
_ErrorDir          = config.get('DIRECTORY', 'ERROR_DIR')
_ConfigDir         = config.get('DIRECTORY', 'CONFIG_DIR')
_ArchiveDir        = config.get('DIRECTORY', 'ARCHIVE_DIR')
_SetupFile         = config.get('FILE', 'SETUP_FILE')
_FileValidatorLog  = config.get('FILE', 'FILE_VALIDATOR_LOG')
_LogLevel          = config.get('LOG', 'LOG_LEVEL')
_db_Prefix         = config.get('DATABASE', 'DB_PREFIX')
_ChunkSize         = int(config.get('DATABASE', 'CHUNK_SIZE'))
_DatePy            = config.get('DATA', 'DATE_PY')
_DateDB            = config.get('DATA', 'DATE_DB')
_EncodingUTF8      = config.get('DATA', 'ENCODING_UTF8')
_EncodingCP1252    = config.get('DATA', 'ENCODING_CP1252')



# #_SqlServerConn     = urllib.parse.quote_plus(config.get('DATABASE', 'SQLSERVER_CONN')) ToDo#1 Find out why assigning this way FAILS but hardcoding below works

_SqlServerConn = os.environ.get('DB_SERVER_CONN_STR') or 'Driver={SQL Server};Server=DESKTOP-P89EVC6;Database=DDI_STAG;trusted_connection=NO'

# #print('type(_SqlServerConn) inside LIB ==> ', type(_SqlServerConn))
# #print('_SqlServerConn inside LIB ==> ', _SqlServerConn)

lib_logger = logging.getLogger(__name__)



def check_decimal(d):
    lib_logger.debug('Begin : Inside check_decimal function')

    if not str(d).strip() or pd.isnull(d):
       return True

    try:
        Decimal(d)
    except InvalidOperation:
        lib_logger.info('Invalid Operation exception raised inside check_decimal function for value : ' + str(d))    
        return False
    finally:
        lib_logger.debug('End : Inside check_decimal function')
        
    return True
	
def check_int(i):
    lib_logger.debug('Begin : Inside check_int function')
       
    if not str(i).strip() or pd.isnull(i):
       return True

    try:
        int(i)
        
        if str(i).find('.') >= 0:
           raise ValueError
           
    except ValueError:
        lib_logger.info('Value Error exception raised inside check_int function for value : ' + str(i))    
        return False
    finally:
        lib_logger.debug('End : Inside check_int function')
    return True

def check_size(txt, num):
    lib_logger.debug('Begin : Inside check_size function')
    
    #print('see txt value => ', txt)
    
    if not str(txt).strip() or pd.isnull(txt):
       return True
    elif (len(str(txt)) > int(num)):
       lib_logger.info('Size Error inside check_size function for text : => ' + str(txt) + ' <= and column size in db validator/target table : ' + str(num))
       return False

    lib_logger.debug('End : Inside check_size function')
    return True

def check_date(dt):
    lib_logger.debug('Begin : Inside check_date function')
    
    #print('see dt value => ', dt)
    
    if not str(dt).strip() or pd.isnull(dt):
       return True
    else:
       try: 
          myDT = pd.to_datetime(dt, format=_DatePy) 
       except ValueError:
          lib_logger.info('Value Error exception raised inside check_date function for value : ' + str(dt))    
          return False
       finally:
          lib_logger.debug('End : Inside check_date function')
    return True

def rowNumber(row):
    return row.name

def getBatchNumber():
    lib_logger.debug('Begin : Get Batch Number')
    #print('_SqlServerConn inside LIB2 ==> ', _SqlServerConn)

    try:
        conn = pypyodbc.connect(_SqlServerConn)
        c = conn.cursor()
        myBatchNumber = 0

        c.execute("select isnull(max(batchnumber), 0) + 1 from ddi_stag.dbo.py_tpon_validation;", (myBatchNumber))
        myBatchNumber = [x[0] for x in c.fetchall()][0]
        #print("see batchNumber => " + str(myBatchNumber))
        lib_logger.info('Batch Number of current pydif Run ==>  ' + str(myBatchNumber))

    except:
       e = sys.exc_info()
       lib_logger.critical('Function "Get Batch Number" failed : ' + str(e))
       raise
    finally:
       conn.close()
       lib_logger.debug('End : Get Batch Number')
    return myBatchNumber

def getTableValidationCriteria(tableName, batchNumber):
    lib_logger.debug('Begin : Generate Table Validation Criteria')

    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()
       table_validation_criteria = ''

       sql = '''
             SET NOCOUNT ON;
             DECLARE @OUTCOME INT;
             EXEC DDI_STAG.DBO.SP_PY_TPON_VALIDATION @TABLE_NAME = ''' + "'" + str(tableName) + "', @BATCHNUMBER = " + str(batchNumber) + ''', @OUTCOME = @OUTCOME OUTPUT;
             SELECT @OUTCOME;'''

       #print(sql)

       #STEP 1(a) : Generate the Table Validation Criteria in DB
       result = c.execute(sql)
       #print(result)
       outcome = result.fetchone()
       #print(outcome[0])
       #print(type(outcome[0]))
    
       if (outcome[0] == 0):
           lib_logger.debug('Begin : Retrieve Table Validation Criteria')
           #STEP 1(b) : Retrieve the Table Validation Criteria in DB
           c.execute("select table_validation_criteria from ddi_stag.dbo.py_tpon_validation where seqnumber = (select max(seqnumber) from ddi_stag.dbo.py_tpon_validation where cast(getdate() as date) = cast(insert_date as date) and load_status = 'SUCCESS' and table_name = ?)", (str(tableName),))
           table_validation_criteria = [x[0] for x in c.fetchall()][0]
            
           #print(table_validation_criteria)
           #print(type(table_validation_criteria))
           lib_logger.debug('End : Retrieve Table Validation Criteria')
    except:
       e = sys.exc_info()
       lib_logger.critical('Function "getTableValidationCriteria" failed with parameters tableName : ' + str(tableName) + ' and batchNumber : ' + str(batchNumber) + ' and raised Exception ==> ' + str(e))
       raise
    finally:        
       conn.close()
       lib_logger.debug('End : Generate Table Validation Criteria')

    return table_validation_criteria  

def getErrorSourceDataDF(myDF, myErrorDF):
    lib_logger.debug('Begin : Extract Source Error Data')
    myErrorSeries = myErrorDF['RowNumber']
    myDF['rowNumber'] = myDF.apply(lambda row : rowNumber(row), axis=1)

    myDFBooleanSeries = myDF["rowNumber"].isin(myErrorSeries.unique())
    myErrorSourceDataDF = myDF[myDFBooleanSeries]
    
    myErrorSourceDataDF = myErrorSourceDataDF.drop(['rowNumber'], axis = 1)
    lib_logger.debug('End : Extract Source Error Data')
    return myErrorSourceDataDF  

def getCleanSourceDataDF(myDF, myErrorDF):
    lib_logger.debug('Begin : Extract Source Clean Data')
    myErrorSeries = myErrorDF['RowNumber']
    myDF['rowNumber'] = myDF.apply(lambda row : rowNumber(row), axis=1)

    myDFBooleanSeries = np.logical_not(myDF["rowNumber"].isin(myErrorSeries.unique()))
    myCleanSourceDataDF = myDF[myDFBooleanSeries]
    
    myCleanSourceDataDF = myCleanSourceDataDF.drop(['rowNumber'], axis = 1)
    lib_logger.debug('End : Extract Source Clean Data')
    return myCleanSourceDataDF  

def getSourceDataDF(myDF):
    lib_logger.debug('Begin : Get Full Source Data')
    mySourceDataDF = myDF.drop(['rowNumber'], axis = 1)
    lib_logger.debug('End : Get Full Source Data')
    return mySourceDataDF  

#def runPythonCodeGenerator(myTableName, mySourceType, mySource, myTarget, myValidationCriteria, myBatchNumber, myMapped):
def runPythonCodeGenerator(myTableName, mySourceType, mySource, myTargetType, myTarget, myValidationCriteria, myBatchNumber, myMapped):

    #STEP 2 : Generate Python Data Validator Code
    lib_logger.debug('Begin : Generate Python File Validation Code')
    pyGeneratedFileWithPath = path.join(".", str(myTableName) + '.py')
    pyLogFileWithPath       = path.join("." , _LogDir + str(myTableName) + '.log')
    pySourceFileWithPath    = path.join(path.dirname(path.dirname(path.dirname(__file__))),  _SourceDir, str(mySource))
    pyTargetFileWithPath    = path.join(".", _TargetDir + str(myTarget))
    
    #print("pyTargetFileWithPath ==> ", pyTargetFileWithPath)
    
    f = open(pyGeneratedFileWithPath, mode="w")
    f.write('''    
import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation, IsDistinctValidation, CustomElementValidation
from py_validator_lib import check_date, setOverallErrorStatus, loadTarget, check_size, check_int, check_decimal, setPyErrorMessage, createDataValidationErrorFile, getColumnDict, getOverallErrorStatus
import numpy as np
import json
import logging
import sys
import ast
    ''')

    f.write('''    
try:
   myLogLevel = ''' + "'" + str(_LogLevel) + "'" + '''
   log_format = "%(asctime)s :: %(levelname)s :: %(name)s :: %(filename)s :: %(lineno)d :: %(message)s"
   logging.basicConfig(filename=''' + "'" + str(pyLogFileWithPath) + "'" + ''', filemode='w', level=myLogLevel, format=log_format)
   pyCode_logger = logging.getLogger(__name__)
   pyCode_logger.info('Begin : Inside Generated Python Code')
    ''')
    
    myColumnSetUpDictList = getColumnSetUpDict(str(myTableName))
    myList = myColumnSetUpDictList.split('***-***')

    dtypeDict = myList[0]
    convertersDict = myList[1]
  
    if (mySourceType.upper() == 'CSV'):
        f.write('''
   myDF = pd.read_csv(''' + '"' + str(pySourceFileWithPath) + '", encoding="' + _EncodingCP1252 + '", dtype=' + dtypeDict + ', converters=' + convertersDict + ')')
    elif (mySourceType.upper() == 'XLS' or mySourceType.upper() == 'XLSX'):
          f.write('''
   myDF = pd.read_excel(''' + '"' + str(pySourceFileWithPath) + '", encoding="' + _EncodingUTF8 + '", dtype=' + dtypeDict + ', converters=' + convertersDict + ')')
    elif (mySourceType.upper() == 'JSON'):
          f.write('''
   json_file = open(''' + '"' + str(pySourceFileWithPath) + '"' + ', "r", encoding="' + _EncodingUTF8 + '"' + ''')
   mySourceDataStr = json.load(json_file)
   json_file.close()
   #mySourceDataDict = lib.cleanJSONSourceDataDDI(mySourceDataDict, ''' + '"' + str(myTableName) + '"' + ''')
   #mySourceDataStr = json.dumps(mySourceDataDict)
   myDF = pd.read_json(mySourceDataStr, dtype=''' + dtypeDict + ''')
   #myDF = lib.cleanJSONDFDDI(myDF)
   #print(myDF.dtypes)
   #print(myDF)

   ''')     
    else:
          raise Exception('Failed. Incorrect Source Type ' + str(mySourceType) + ' Please, check the SetUp File Information')

    if (str(myMapped).upper() == 'YES'):
        myColumnDict = getColumnDict(myTableName)
        f.write('''
   myDF.rename(columns=''' + str(myColumnDict) + ''', inplace=True)
    ''')     

    schema = str(myValidationCriteria)
    f.write('''
   myDF = myDF.applymap(lambda x: x.strip() if isinstance(x, str) else x)
   schema = Schema(''' + str(schema) + ')')
	
    f.write('''
   myErrorDir = ''' + "'" + str(_ErrorDir) + "'" + '''
   errors = schema.validate(myDF)
   errCount = len(errors)
   #print('len(errors) ===> ', len(errors))
    ''')

    f.write('''
   row = []
   col = []
   val = []
   err = []

   if len(errors) > 0:
      for e in errors:
          row.append(e.row)
          col.append(str(e.column))
          val.append(str(e.value))
          err.append(str(e.message))

      dict = {'RowNumber' : row, 'ColumnName' : col, 'ColumnValue' : val, 'ErrorMessage' : err}  

      myErrorDF = pd.DataFrame(dict) 
      myDFCopy  = myDF.copy(deep=True)
      pyCode_logger.info('Begin : Creating Data Validation Error file')
      pyDataValidationErrorFile = createDataValidationErrorFile(myDFCopy, myErrorDF, ''' + "'" + myTableName + "', " + str(myBatchNumber) + ", '" + str(mySource) + "', '" + str(myTarget) + "'" + ''')
      pyCode_logger.info('End : Creating Data Validation Error file')

      errMessage = 'Please, check the Source Data Validation Error Outcome file ' + str(pyDataValidationErrorFile) + ' in directory "' + str(myErrorDir) + '" for ' + str(errCount) + ' Validation Error(s) *** '
      #print("errMessage => ", errMessage)
      setPyErrorMessage(errMessage, ''' + "'" + myTableName + "', " + str(myBatchNumber) + ''')
   else:
       pyCode_logger.info('Begin : Load Target => ''' + str(myTarget) + '''')
       pyCode_logger.info('Load Target for Batch Number => ''' + str(myBatchNumber) + '''')
       
       overallErrorStatus = 0
       overallErrorStatus = getOverallErrorStatus(''' + str(myBatchNumber) + ''')
       pyCode_logger.info('Overall Error Status before Target Load => ' + str(overallErrorStatus)) 
       
       if (overallErrorStatus == 0):
          returnValue = loadTarget(''' + "'" + str(myTargetType) + "', '" + str(myTableName) + "', '" + str(pyTargetFileWithPath) + "', '" + str(myTarget) + '''', myDF)

          pyCode_logger.info('Return Value of Target Load Call => ' + str(returnValue)) 
          if (returnValue != 0):
              myErrMessage = 'Loading data for Target: ''' + str(myTarget) + " failed as current Batch# : " + str(myBatchNumber) + ''' encountered Error'
              setOverallErrorStatus(''' + str(myBatchNumber) + ''', myErrMessage)
              pyCode_logger.info(myErrMessage)
              
       pyCode_logger.info('End : Load Target => ''' + str(myTarget) + '''')
    ''')
    f.write('''
   pyCode_logger.info('End : Inside Generated Python Code')
   
except:
   e = sys.exc_info()
   e = str(e).replace("'", '"')
   pyCode_logger.info('Begin : Inside Exception Block')
   print('Exception => ' + str(e))
   #myErrMessage = 'Current Batch# : ' + str(myBatchNumber) + ' encountered an Exception : ' + str(e) + ' Please, check the Logs'
   #lib.setOverallErrorStatus(myBatchNumber, myErrMessage)
   pyCode_logger.critical('function "runPythonCodeGenerator" raised Exception ==> ' + str(e))
   pyCode_logger.info('End : Inside Exception Block')
   raise

finally:
   pyCode_logger.info('Begin : Inside Finally Block')
   #print('In finally block for cleanup')
   pyCode_logger.info('End : Inside Finally Block')
   ''')

    f.close()
    lib_logger.debug('End : Generate Python File Validation Code')

def createDataValidationErrorFile(myDF, myErrorDF, myTableName, myBatchNumber, mySource, myTarget):
    lib_logger.debug('Begin : Create Source Error Data Excel file')
        
    # Generate the Error Log File 
    now = datetime.datetime.now()
    pyDataValidationErrorFile = str(myTableName) + '_' + str(myBatchNumber) + '_' + str(now.strftime("%d-%m-%Y_%H-%M-%S")) + '.xlsx'
    pyDataValidationErrorFileWithPath = path.join(".", _ErrorDir + str(pyDataValidationErrorFile))
    #print(pyDataValidationErrorFile)
    
    # Create excel writer object
    writer = pd.ExcelWriter(pyDataValidationErrorFileWithPath)

    # Write dataframe to excel sheet named 'ErrorLog'
    myErrorDF.to_excel(writer, 'ErrorLog', encoding=_EncodingUTF8, index=False)
    
    # Save ErrorLog to database
    saveErrorLog2DB(myErrorDF, myTableName, myBatchNumber, mySource, myTarget)

    # Write the dataframe to excel sheet named 'ErrorSourceData'
    myErrorSourceDataDF = getErrorSourceDataDF(myDF, myErrorDF)
    myErrorSourceDataDF.to_excel(writer, 'ErrorSourceData', encoding=_EncodingUTF8)
       
    # Write the dataframe to excel sheet named 'CleanSourceData'
    myCleanSourceDataDF = getCleanSourceDataDF(myDF, myErrorDF)
    myCleanSourceDataDF.to_excel(writer, 'CleanSourceData', encoding=_EncodingUTF8)

    # Write dataframe to excel sheet named 'SourceData'
    myDF = myDF.drop(['rowNumber'], axis = 1)
    myDF.to_excel(writer, 'SourceData', encoding=_EncodingUTF8)
    
    # Save the excel file
    writer.save()
    lib_logger.debug('End : Create Source Error Data Excel file')
    return pyDataValidationErrorFile

def setPyErrorMessage(errMessage, myTableName, myBatchNumber):
    # Update the Log table
    lib_logger.debug('Begin : Set Python Error Message')
    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       #print("errMessage => ", errMessage)

       sql = '''
             UPDATE DDI_STAG.DBO.PY_TPON_VALIDATION SET PY_ERROR_MESSAGE = ISNULL(PY_ERROR_MESSAGE, '*** ') + ''' + "'" + str(errMessage) + "'" + " WHERE SEQNUMBER = (SELECT MAX(SEQNUMBER) FROM DDI_STAG.DBO.PY_TPON_VALIDATION) AND TABLE_NAME = " + "'" + str(myTableName) + "' AND BATCHNUMBER = " + str(myBatchNumber) + ''';
             COMMIT;'''
       #print("sql => ", sql)
       c.execute(sql)
    except:
       e = sys.exc_info()
       lib_logger.critical('Function "setPyErrorMessage" failed for parameters tableName : ' + str(myTableName) + ' and batchNumber : ' + str(myBatchNumber) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       conn.close()
    lib_logger.debug('End : Set Python Error Message')

def getOverallErrorStatus(myBatchNumber):
    lib_logger.debug('Begin : Get Python Overall Error Status')
    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       sql = "SELECT ISNULL(COUNT(*), 0) FROM DDI_STAG.DBO.PY_TPON_VALIDATION WHERE BATCHNUMBER = " + str(myBatchNumber) + " AND (PY_ERROR_MESSAGE IS NOT NULL OR ERRORMESSAGE IS NOT NULL);"
       #print("sql => ", sql)
       result = c.execute(sql)
       outcome = result.fetchone()
       #print("outcome[0] => ", outcome[0])
    except:
       e = sys.exc_info()
       lib_logger.critical('Function "getOverallErrorStatus" failed for parameter batchNumber : ' + str(myBatchNumber) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       conn.close()
       
    lib_logger.debug('End : Get Python Overall Error Status')
    return outcome[0]

def setOverallErrorStatus(myBatchNumber, myErrMessage):
    lib_logger.debug('Begin : Set Python Overall Error Status')
    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       sql = '''
             UPDATE DDI_STAG.DBO.PY_TPON_VALIDATION SET PY_ERROR_MESSAGE = ISNULL(PY_ERROR_MESSAGE, '*** ') + ''' + "'" + str(myErrMessage) + "'" + " WHERE SEQNUMBER = (SELECT MAX(SEQNUMBER) FROM DDI_STAG.DBO.PY_TPON_VALIDATION) AND BATCHNUMBER = " + str(myBatchNumber) + ''';
             COMMIT;'''
       #print("sql => ", sql)
       c.execute(sql)
    except:
       e = sys.exc_info()
       lib_logger.critical('Function "setOverallErrorStatus" failed for parameter batchNumber : ' + str(myBatchNumber) + ' and raised Exception ==> ' + str(e))
       raise
    finally:    
        conn.close()
        
    lib_logger.debug('End : Set Python Overall Error Status')
    
def loadTarget(myTargetType, myTable, pyTargetFileWithPath, myTarget, mySourceDF):
    lib_logger.debug('Begin : Inside Load Target')
    returnValue = 0
    
    mySourceDFTarget = mySourceDF.dropna(axis=0, how='all')
    mySourceDFTarget = mySourceDFTarget.drop_duplicates() 
    
    if (myTargetType.upper() == 'CSV'):
        mySourceDFTarget.to_csv(str(pyTargetFileWithPath), encoding=_EncodingCP1252, index=False) 
        
    elif (myTargetType.upper() == 'XLS' or myTargetType.upper() == 'XLSX'):
        writer = pd.ExcelWriter(pyTargetFileWithPath)
        #print("see pyTargetFileWithPath ==> ", pyTargetFileWithPath)
        mySourceDFTarget.to_excel(writer, str(myTable), encoding=_EncodingUTF8, index=False)
        writer.save()

    elif (myTargetType.upper() == 'JSON'):
        mySourceDFTarget.to_json(pyTargetFileWithPath)        
        
    elif (myTargetType.upper() == 'DB'): 
        try:
            myTargetWithDBPrefix = _db_Prefix + str(myTarget)        
            sqlTrunc = "TRUNCATE TABLE " + str(myTargetWithDBPrefix) + "; COMMIT;"
            #print(sqlTrunc)
        
            db_params = urllib.parse.quote_plus(_SqlServerConn)
            engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(db_params))

            conn = engine.connect().connection
            cursor = conn.cursor()

            cursor.execute(sqlTrunc)
 
            myCol = ''
            for col in mySourceDFTarget.columns.values:
                if (not myCol):
                    myCol = str(col)
                else:
                    myCol = myCol + ', ' + str(col)
            myCol = '(' + myCol + ')'

            sql = str("SET DATEFORMAT " + _DateDB + "; INSERT INTO " + str(myTargetWithDBPrefix) + ' ' + myCol + " VALUES ").upper()
        
            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                   cursor.fast_executemany = True
        
            i = 0
            j = 0
            index = 0
            number_of_rows = 0
            while (i <= len(mySourceDFTarget)):        
                j = i + _ChunkSize
                recordsInsertDF = mySourceDFTarget.iloc[i:j,:]
            
                index = recordsInsertDF.index
                number_of_rows = len(index)
                #print('number_of_rows => ', number_of_rows)
                if number_of_rows > 0:
                   sqlInsert =  chunkerInsert(sql, recordsInsertDF)
                   sqlInsert = sqlInsert.upper()
                   #print(sqlInsert)
                   sqlInsert = sqlInsert.replace('NONE', 'NULL')
                   sqlInsert = sqlInsert.replace('NAN', 'NULL')
                   sqlInsert = str(sqlInsert) + "; COMMIT;"
                   #print("sqlInsert " + str(i) + " => ", sqlInsert)
                   #create atemp df from the sqlinsert and pass it on to to_sql            
                   #tbl = _db_Prefix + myTable
                   #recordsInsertDF.to_sql(tbl, engine, chunksize = _ChunkSize) 
                   #recordsInsertDF.to_sql(myTable, engine, chunksize = _ChunkSize, index=False, if_exists="append", schema=str(_db_Prefix))
                   #print('sqlInsert => ', sqlInsert)
                   cursor.execute(sqlInsert)
                   #recordsInsertDF = pd.DataFrame
                i = j
        except:
           e = sys.exc_info()
           lib_logger.critical('Function "loadTarget" for DB failed with parameter tableName : ' + str(myTable) + ' and raised Exception ==> ' + str(e))
           raise
        finally:
           conn.close()
        
    else:
        returnValue = 1
        lib_logger.debug('Failed. Incorrect Target Type ' + str(myTargetType) + ' Please, check the SetUp File Information')
        raise Exception('Failed. Incorrect Target Type ' + str(myTargetType) + ' Please, check the SetUp File Information')
    
    lib_logger.debug('End : Inside Load Target')
    return returnValue
  
def chunkerInsert(sql, dfInsert):
    lib_logger.debug('Begin : Inside Chunker Insert')
    #print('Begin : Inside Chunker Insert')

    for aRecord in dfInsert.values:
        #print("aRecord => ", aRecord)  
        #print("type(aRecord) => ", type(aRecord))  
                 
        aRecordStr = ''
        if (str(aRecord).count('"') >= 1):
            aRecordStr = removeSingleQuote(aRecord)
            #print('strARecord inside chunker insert 1 => ', aRecordStr)                      
            sql = sql + aRecordStr + ', '
        else:    
            sql = sql + str(tuple(aRecord)) + ', '  
        #print("see sql 1 => ", sql)
        #print('aRecord as tuple 2 => ', str(tuple(aRecord)))                      
        
    sql = sql[:sql.rfind(',')]
    #print("see sql 2 => ", sql)
    lib_logger.debug('End : Inside Chunker Insert')
    #print('End : Inside Chunker Insert')
    return sql

def removeSingleQuote(aRecord):
    lib_logger.debug('Begin : Remove Single Quote')

    #print('tuple => ', tuple(aRecord))
    #print('string of tuple => ', str(tuple(aRecord)))
              
    strARecord = ''
    i = 0
    for aTuple in tuple(aRecord):
        
        strATuple = str(aTuple)
        if str(type(aTuple)).count('str'):
           if strATuple.count("'") > 0:
              #print('strATuple => ', strATuple) 
              strATuple = strATuple.replace("'", "''")
           if i == 0:
              strARecord = "'" + strATuple + "'" 
           else:
              strARecord = strARecord + ", " + "'" + strATuple + "'" 
           i = i + 1
        else:
              if i == 0:
                 strARecord = strATuple 
              else:
                 strARecord = strARecord + ", " + strATuple 
              i = i + 1                          
                          
    strARecord = "(" + strARecord + ")"    
    #print('strARecord inside remove-single-quote => ', strARecord)              

    lib_logger.debug('End : Remove Single Quote')
    return strARecord    

def getColumnDict(myTableName): 
    lib_logger.debug('Begin : Get Column Mapping Dictionary')
    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       sql = "SELECT DISTINCT COLUMN_DICT FROM DDI_STAG.DBO.PY_MAPPING_SETUP WHERE TABLE_NAME = " + "'" + str(myTableName) + "'" + ";"
       #print("sql => ", sql)
       result = c.execute(sql)

       outcome = result.fetchone()
       myColumnDictStr = outcome[0]
    except TypeError:
       e = sys.exc_info()
       lib_logger.critical('Function "getColumnDict" failed with parameter tableName : ' + str(myTableName) + ' and raised Exception ==> ' + str(e))
       raise ce.noColumnMappingException("No existing source-target Column Mapping information found. Please, check the Mapped column of py_validator_Setup file for table : " + myTableName)    
    except Exception:
       e = sys.exc_info()
       lib_logger.critical('Function "getColumnDict" failed with parameter tableName : ' + str(myTableName) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       conn.close()
      
    lib_logger.debug('End : Get Column Mapping Dictionary')
    return myColumnDictStr

def getColumnSetUpDict(myTableName): 
    lib_logger.debug('Begin : Get Column SetUp Dictionary')
    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       #sql = "SELECT " + "'[' + DTYPE_DICT + " + "', '" + " + CONVERTERS_DICT + ']'" + " FROM " + _db_Prefix + "PY_COLUMN_SETUP WHERE TABLE_NAME = " + "'" + str(myTableName) + "'" + ";"
       sql = "SELECT " + "DTYPE_DICT + " + "'***-***'" + " + CONVERTERS_DICT" + " FROM " + _db_Prefix + "PY_COLUMN_SETUP WHERE TABLE_NAME = " + "'" + str(myTableName) + "'" + ";"
       #print("myColumnSetUpDictList sql => ", sql)
       result = c.execute(sql)

       outcome = result.fetchone()
       myColumnSetUpDictList = outcome[0]
    except TypeError:
       e = sys.exc_info()
       lib_logger.critical('Function "getColumnSetUpDict" failed with parameter tableName : ' + str(myTableName) + ' and raised Exception ==> ' + str(e))
       raise ce.noColumnSetUpException("Failed to retrieve Column SetUp information for table : " + myTableName)    
    except Exception:
       e = sys.exc_info()
       lib_logger.critical('Function "getColumnSetUpDict" failed with parameter tableName : ' + str(myTableName) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       conn.close()
      
    lib_logger.debug('End : Get Column SetUp Dictionary')
    return myColumnSetUpDictList

def getLastValidationCriteria(myTable, myBatchNumber):
    lib_logger.debug('Begin : Set & Get Last Validation Criteria')

    try:

       db_params = urllib.parse.quote_plus(_SqlServerConn)
       engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(db_params))       
       conn = engine.connect()                      
    
       sqlSetLast = '''
          SET NOCOUNT ON;
          EXEC ''' + str(_db_Prefix) + "SP_PY_GET_LAST_VALIDATION_CRITERIA @TABLE_NAME = " + "'" + str(myTable) + "', @BATCHNUMBER = " + str(myBatchNumber) + ''';
          '''
       result = engine.execute(sqlSetLast)

       table_validation_criteria = ''
       sqlGetLast = '''
          SELECT DISTINCT RTRIM(TABLE_VALIDATION_CRITERIA) FROM ''' + str(_db_Prefix) + "PY_TPON_VALIDATION WHERE TABLE_NAME = '" + str(myTable) + "' AND BATCHNUMBER = " + str(myBatchNumber) + ";"
    
       #print('sqlGetLast => ', sqlGetLast)
       result = engine.execute(sqlGetLast)
    
       table_validation_criteria = result.first()[0]
    except TypeError:
       e = sys.exc_info()
       lib_logger.critical('Function "getLastValidationCriteria" failed with parameter tableName : ' + str(myTable) + ' and raised Exception ==> ' + str(e))
       raise ce.noValidationCriteriaException("No existing validation criteria was found. Please, check the Generate_Criteria column of py_validator_Setup file for table : " + myTable)
    except Exception:
       e = sys.exc_info()
       lib_logger.critical('Function "getLastValidationCriteria" failed with parameter tableName : ' + str(myTable) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       #print('in finally')
       conn.close()
        
    lib_logger.debug('End : Set & Get Last Validation Criteria')

    return table_validation_criteria  

def saveErrorLog2DB(myErrorDF, myTableName, myBatchNumber, mySource, myTarget):
    lib_logger.debug('Begin : Save ErrorLog to database table')
    try:
       errorLogTable = 'PY_DATAFILE_ERRORLOG'
       #print("inside saveErrorLog2DB")
    
       db_params = urllib.parse.quote_plus(_SqlServerConn)
       engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(db_params))
       conn = engine.connect().connection
       cursor = conn.cursor()       
    
       myErrorDFCopy = myErrorDF.copy()                
       myErrorDFCopy.columns = map(str.upper, myErrorDFCopy.columns)
       myErrorDFCopy.insert(0, "BATCHNUMBER", myBatchNumber, True)
       myErrorDFCopy.insert(1, "SOURCE_NAME", str(mySource), True)
       myErrorDFCopy.insert(2, "TARGET_NAME", str(myTarget), True)
       myErrorDFCopy.insert(3, "VALIDATOR_TABLE", str(myTableName), True)

       myTargetWithDBPrefix = _db_Prefix + str(errorLogTable)        
 
       myCol = ''
       for col in myErrorDFCopy.columns.values:
           if (not myCol):
               myCol = str(col)
           else:
               myCol = myCol + ', ' + str(col)
       myCol = '(' + myCol + ')'

       sql = str("INSERT INTO " + str(myTargetWithDBPrefix) + ' ' + myCol + " VALUES ").upper()
        
       @event.listens_for(engine, "before_cursor_execute")
       def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
           if executemany:
              cursor.fast_executemany = True
        
       i = 0
       j = 0
       index = 0
       number_of_rows = 0
       while (i <= len(myErrorDFCopy)):        
           j = i + _ChunkSize
           recordsInsertDF = myErrorDFCopy.iloc[i:j,:]

           index = recordsInsertDF.index
           number_of_rows = len(index)
           if number_of_rows > 0:
              sqlInsert = chunkerInsert(sql, recordsInsertDF)
              sqlInsert = sqlInsert.upper()
              sqlInsert = sqlInsert.replace('NONE', 'NULL')
              sqlInsert = sqlInsert.replace('NAN', 'NULL')
              sqlInsert = str(sqlInsert) + "; COMMIT;"

              #print('sqlInsert => ', sqlInsert)
              cursor.execute(sqlInsert)
           i = j      
    except Exception:
       e = sys.exc_info()
       lib_logger.critical('Function "saveErrorLog2DB" failed with parameter tableName : ' + str(myTableName) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       conn.close()

    lib_logger.debug('End : Save ErrorLog to database table')

def createDirectory(dirPath, dirName):
    lib_logger.debug('Begin : Create directory')
    path = str(dirPath) + str(dirName)
    os.mkdir(path)
    lib_logger.debug('End : Create directory')
    
def copyDirectory(sourceDir, targetDir):
    lib_logger.debug('Begin : Move from Source to Target directory')
    #print(sourceDir)
    #print(targetDir)
    try:
        shutil.copytree(sourceDir, targetDir)
    # Directories are the same
    except shutil.Error as e:
        lib_logger.debug('Directory not copied. Error: %s' % e)
        #raise
    # Any error saying that the directory doesn't exist
    except OSError as e:
        lib_logger.debug('Directory not copied. Error: %s' % e)
        #raise
    lib_logger.debug('End : Move from Source to Target directory')

def rmAllFiles(targetDir):
    lib_logger.debug('Begin : Remove all files from directory')
    #print(targetDir)
    fileList = os.listdir(targetDir)
    for fileName in fileList:
        #print(fileName)
        os.remove(targetDir + fileName)
    lib_logger.debug('End : Remove all files from directory')

def runSQL(mySQL):
    try:
       lib_logger.debug('Begin : Run Sql')
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       #print("inside runSQL => ", mySQL)
       c.execute(mySQL)
    except Exception:
       e = sys.exc_info()
       lib_logger.critical('Function "runSQL" failed with parameter mySQL : ' + str(mySQL) + ' and raised Exception ==> ' + str(e))
       raise
    finally:
       conn.close()
       
    lib_logger.debug('End : Run Sql')

def truncateAllLandingTables():
    lib_logger.debug('Begin : Truncate all Landing tables')
    try:
       conn = pypyodbc.connect(_SqlServerConn)
       c = conn.cursor()

       sql = 'EXEC ' + _db_Prefix + 'SP_PY_LNDG_TRUNCATE;'
       #print("sql => ", sql)
       
       c.execute(sql)
    except:
       e = sys.exc_info()
       lib_logger.error('Function "truncateAllLandingTables" failed' + ' and raised Exception ==> ' + str(e))
    finally:
       conn.close()
    lib_logger.debug('End : Truncate all Landing tables')
