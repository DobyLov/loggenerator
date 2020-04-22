"""
Gestionnaire de fichier de Logz 
-- log persistance sur fichier avec l' argurment fname
-- Error log
-- Enrengstrer le s logs dans un fs
"""

from datetime import datetime
from log_generator.dateTime_handler import get_dateNow
from log_generator.files_handler import write_file
from log_generator.dateTime_handler import get_date_onlyDate_now


# Ecrire dans le fichier de persistance des logs enseigné par 
# l'argument au lancement de la ligne de commande
def log2File(output_text: str, file_path_name: str):
     write_file(file_path_name, output_text)

# Write log file from http get error
def errorLog(message :str, file_path_name:str):
    #global http_pathLogErrorFile
    fullErrorMsg = str(datetime.now()) + "\t" + str(message)
    write_file(file_path_name, fullErrorMsg)

