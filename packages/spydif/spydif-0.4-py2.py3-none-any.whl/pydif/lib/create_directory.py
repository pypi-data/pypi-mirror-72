import os
import os.path as path
from configparser import ConfigParser

def make_folder(folder_name):
    """
    create folder for the given folder name if does not exist

    """
    if not path.exists(folder_name):
        os.makedirs(path.join(".", folder_name))

config = ConfigParser()
myConfigFileOSPath = path.join(path.dirname(path.dirname(__file__)), 'config', 'py_validator_config.cfg')
# print(myConfigFileOSPath)
config.read(myConfigFileOSPath)

_LogDir            = config.get('DIRECTORY', 'LOG_DIR')
_TargetDir         = config.get('DIRECTORY', 'TARGET_DIR')
_ErrorDir          = config.get('DIRECTORY', 'ERROR_DIR')
_ArchiveDir        = config.get('DIRECTORY', 'ARCHIVE_DIR')

make_folder(_LogDir)
make_folder(_TargetDir)
make_folder(_ErrorDir)
make_folder(_ArchiveDir)
