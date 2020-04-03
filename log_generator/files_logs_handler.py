"""
Gestionnaire de fichier de Logz 
-- log persistance sur fichier avec l' argurment fname
-- Error log
-- Enrengstrer le s logs dans un fs
"""

from datetime import datetime
from log_generator.dateTime_handler import get_dateNow


# Ecrire dans le fichier de persistance des logs enseigné par 
# l'argument au lancement de la ligne de commande
def log2File(output_text: str, filePath: str):
    print("ecriture du fichier log")
    try:
        file = open(filePath, "a")
        file.write(output_text + "\n")
    except OSError as err:
        print("OS error: {0}".format(err))

# Write log file from http get error
def errorLog(message :str, file_path:str):
    #global http_pathLogErrorFile
    fullErrorMsg = str(datetime.now()) + "\t" + str(message)
    try:
        file = open(file_path, "a")
        file.write(fullErrorMsg + "\n")
    except OSError as err:
        print("OS error: {0}".format(err))

