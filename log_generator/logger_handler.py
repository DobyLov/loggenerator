""" Logger handler """

import logging
import logging.config
from log_generator.files_handler import file_exist_check, remove_file, write_file, read_file

fileName = "logLevel.txt"

def logger_configurator():
    levelLogging:int
    if file_exist_check(fileName):
        levelLoggin_str = get_logLevel_from_file()
        levelLogging = logLevel_Converter(levelLoggin_str)
    else:
        #delete_file_log_level(fileName)
        levelLoggin_str = "ERROR"
        levelLogging = 40
        create_file_log_level(levelLoggin_str)
        
    return logging.basicConfig(
                        filename="./loggen_" + levelLoggin_str + ".log",
                        level=levelLogging,
                        format='%(asctime)s  %(name)s  %(levelname)s: %(message)s'
                        )

# Recupere le contenu du fichier logLevel 
def get_logLevel_from_file():
    return line_filter_from_file( 
        read_file(fileName)
    )

# Convert string logLevel into int logLevel
def logLevel_Converter(level:str):
    level_int:int = 0
    if level == "CRITICAL":
        level_int = 50
    elif level == "ERROR":
        level_int = 40
    elif level == "WARNING":
        level_int = 30
    elif level == "INFO":
        level_int = 20
    elif level == "DEBUG":
        level_int = 10
    elif level == "NOTSET":
        level_int == 0
    return level_int

def check_exist_log_level():
    if file_exist_check(fileName):
        delete_file_log_level(fileName)
        #create_file_log_level("ERROR")

def create_file_log_level(logLevel:str):
    write_file(fileName, logLevel)

def delete_file_log_level(fileName:str):
    remove_file(fileName)

def line_filter_from_file(line:str):
    return line.rstrip()