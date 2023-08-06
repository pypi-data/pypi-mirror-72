import pandas as pd
from pydif.lib import py_validator_lib as lib
import subprocess
import sys
import logging
import datetime
import os
import os.path as path

_LogDir            = lib._LogDir
_SourceDir         = lib._SourceDir
_TargetDir         = lib._TargetDir
_ErrorDir          = lib._ErrorDir
_ConfigDir         = lib._ConfigDir
_ArchiveDir        = lib._ArchiveDir
_SetupFile         = lib._SetupFile
_FileValidatorLog  = lib._FileValidatorLog
_LogLevel          = lib._LogLevel
_db_Prefix         = lib._db_Prefix
_DatePy            = lib._DatePy
_DateDB            = lib._DateDB
_EncodingUTF8      = lib._EncodingUTF8
_EncodingCP1252    = lib._EncodingCP1252

#_SqlServerConn     = urllib.parse.quote_plus(lib._SqlServerConn) ToDo : 

#print('_SqlServerConn inside pydif ==> ', _SqlServerConn)
#print('_db_Prefix => ', _db_Prefix)

logFormat = "%(asctime)s :: %(levelname)s :: %(name)s :: %(filename)s :: %(lineno)d :: %(message)s"
myLogFileWithPath = path.join(".", str(_LogDir), str(_FileValidatorLog))
#print(_LogDir)
#print(_FileValidatorLog)
#print(myLogFileWithPath)
logging.basicConfig(filename=myLogFileWithPath, filemode='w', level=_LogLevel, format=logFormat)
logger = logging.getLogger(__name__)

def main():
    
    try:
       logger.info('Begin : Inside main() Function')
       startTime = datetime.datetime.now()

       mySetUpDF = pd.read_csv(path.join(path.dirname(__file__), _ConfigDir,  _SetupFile))

       myBatchNumber = 0
       myBatchNumber = lib.getBatchNumber()
       overallErrorStatus = 0
       #print(str(myBatchNumber))

       #STEP 1: Create Folder and Archive Files 
       logger.info('Begin : Step#1. Archival-1 process')
       now = datetime.datetime.now()
       dirPath = path.join(".", _ArchiveDir)
       dirName = str(myBatchNumber) + '_' + str(now.strftime("%d-%m-%Y_%H-%M-%S"))
       os.makedirs(path.join(dirPath, dirName))

       currentArchiveDir = dirPath + "/" + dirName + '/'
       # Copy Target Directory
       archiveTargetDir = currentArchiveDir + 'target'
       lib.copyDirectory(path.join(".", _TargetDir), archiveTargetDir)
       # Copy Error Directory 
       archiveErrorDir = currentArchiveDir + 'error'
       lib.copyDirectory(path.join(".",_ErrorDir), archiveErrorDir)
       # Copy Log Directory 
       archiveErrorDir = currentArchiveDir + 'log'
       lib.copyDirectory(path.join(".",_LogDir), archiveErrorDir)
          
       # Delete all Target Files
       lib.rmAllFiles(path.join(".", _TargetDir))
       # Delete all Error Files
       lib.rmAllFiles(path.join(".",_ErrorDir))
    
       # Truncate all Landing tables
       lib.truncateAllLandingTables()
       
       logger.info('End : Step#1. Archival-1 process')

       i = 0
       while (i < len(mySetUpDF.index)): 
           myValidationCriteria = ''  
           mySource             = ''
           myTarget             = ''
           myTable              = ''
           mySourceType         = ''
           myTargetType         = ''
           myActive             = ''
           errMessage           = ''
           myGenerateCriteria   = ''
           myMapped             = ''
           returnValue          = 0
    
           mySource           = mySetUpDF.iloc[i, 0]
           myTarget           = mySetUpDF.iloc[i, 1]
           myTable            = mySetUpDF.iloc[i, 2]
           mySourceType       = mySetUpDF.iloc[i, 3]
           myTargetType       = mySetUpDF.iloc[i, 4]
           myActive           = mySetUpDF.iloc[i, 5]
           myGenerateCriteria = mySetUpDF.iloc[i, 6]
           myMapped           = mySetUpDF.iloc[i, 7]
           
           if (str(myActive).upper() == 'YES'):
              #print(myTable)
              #print(mySource)
              logger.info('Begin : Inside WHILE Loop with i ==>> ' + str(i) + ' and table ==>> ' + str(myTable))
              #tmp = _SourceDir + mySource
              
              if os.path.isfile(path.join(path.dirname(path.dirname(__file__)),_SourceDir, mySource)) == False:
                 raise Exception("Source File was not found. Please, check the Source column of py_validator_Setup file for Source : " + mySource)
                                 
              #print(mySource.rsplit('.', 1)[1].upper())
              if mySource.rsplit('.', 1)[1].upper() != mySourceType.upper():
                 raise Exception("Extension of Source File does not match with Source Type. Please, check the Source and Source_Type column of py_validator_Setup file for Source : " + mySource)                  

              #STEP 2 : (a) Generate & (b) Retrieve the Table Validation Criteria in DB
              logger.info('Begin : Step#2. Generate & Retrieve Table Validation Criteria')
              if (myGenerateCriteria.upper() == 'YES'):
                  myValidationCriteria = lib.getTableValidationCriteria(myTable, myBatchNumber)
              else:
                  myValidationCriteria = lib.getLastValidationCriteria(myTable, myBatchNumber)
              logger.info('End : Step#2. Generate & Retrieve Table Validation Criteria')
              #print('myValidationCriteria => ' + myValidationCriteria)
        
              #STEP 3 : Generate Python Data Validator Code
              logger.info('Begin : Step#3. Generate Python Data Validator Code')
              if (str(myValidationCriteria).isspace == True or len(myValidationCriteria) <= 9 or myValidationCriteria.find('Column') <= 0):
                  returnValue = 1
                  errMessage = 'Generating/Retrieving Validation Criteria' + ' for table ' + myTable + ' Failed. Please, check PY_TPON_VALIDATION table in DB'
                  #print(errMessage)
                  lib.setPyErrorMessage(errMessage, myTable, myBatchNumber)
              else:
                  #lib.runPythonCodeGenerator(myTable, mySourceType, mySource, myTarget, myValidationCriteria, myBatchNumber, myMapped)
                  lib.runPythonCodeGenerator(myTable, mySourceType, mySource, myTargetType, myTarget, myValidationCriteria, myBatchNumber, myMapped)
              logger.info('End : Step#3. Generate Python Data Validator Code')
    
              #STEP 4 : Run the generated Python Data Validator code
              logger.info('Begin : Step#4. Run generated Python Data Validator Code')
              if returnValue == 0:
                 code_path = path.abspath(str(myTable) + ".py")
                 cmd = "python " + code_path
                 #print('cmd: ', cmd)    
                 returned_value = subprocess.call(cmd, shell=True)
                 #returned_value = subprocess.check_output(cmd, shell=True)
                 #print('returned value from subprocess ==> ', str(returned_value))
                 
                 if int(returned_value) != 0:
                    returnValue = 1
                    errMessage = 'Executing generated Python code FAILED with returned value: ' + str(returned_value) + ' Please, check the Python Logs ***'
                    lib.setPyErrorMessage(errMessage, myTable, myBatchNumber)
                 
              logger.info('End : Step#4. Run generated Python Data Validator Code')
              logger.info('End : Inside WHILE Loop with i ==>> ' + str(i) + ' and table ==>> ' + str(myTable))
              
           i = i + 1

       #STEP 5: Create Folder and Archive Files 
       logger.info('Begin : Step#5. Archival-2 process')
       if (returnValue == 0):
          # Copy Source Directory
          archiveSourceDir = currentArchiveDir + 'data'
          lib.copyDirectory(path.join(path.dirname(__file__), _SourceDir), archiveSourceDir)
    
          # Delete all Source Files
          ###################lib.rmAllFiles(_SourceDir)

       logger.info('End : Step#5. Archival-2 process')
       logger.info('End : Inside main() Function')

       return returnValue
          
    except:
       e = sys.exc_info()
       e = str(e).replace("'", '"')
       logger.info('Begin : Inside Exception Block')
       returnValue = 1 
       #print('Exception Block => ' + str(e))
       myErrMessage = 'Current Batch# : ' + str(myBatchNumber) + ' encountered an Exception : ' + str(e) + ' Please, check the Logs'
       lib.setOverallErrorStatus(myBatchNumber, myErrMessage)
       
       logger.info('Exception Block => ' + str(e))
       logger.info('End : Inside Exception Block')
       return returnValue

    finally:
       logger.info('Begin : Inside Finally Block')
       #print('In finally block for cleanup')
       if returnValue == 1:
          # Delete all Target Files
          lib.rmAllFiles(path.join(".", _TargetDir))
          
          # Copy Source Directory
          archiveSourceDir = currentArchiveDir + 'data'
          lib.copyDirectory(path.join(path.dirname(path.dirname(__file__)), _SourceDir), archiveSourceDir)
    
          # Delete all Source Files
          ######################lib.rmAllFiles(_SourceDir)

          # Truncate all Landing tables
          lib.truncateAllLandingTables()
       
       elapsedTime = datetime.datetime.now() - startTime
       logger.info('Total Execution Time (hh:mm:ss.ms) => {}'.format(elapsedTime))
       logger.info('End : Inside Finally Block')


