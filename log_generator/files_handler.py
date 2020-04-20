""" Gestion de fichiers """

from log_generator.exit_program import exitProgram
from zipfile import ZipFile
import os.path
import shutil

# Verification de la presence du fichier
def file_exist_check(file_with_path:str):
    status:bool = False
    try:
        status = os.path.exists(file_with_path)
    except OSError:
        print("File handler: Check file exist: " + file_with_path + " fichier non trouve")
    
    return status

# Verification de la presence du fichier
def file_exist_check_ifNot_exit(file_with_path:str):
    try:
        status = os.path.exists(file_with_path)
        if not status:
            print("File handler: Check file exist: " + file_with_path + " fichier non trouve")
            exitProgram() 

    except OSError:
        print("File handler: Check file exist: " + file_with_path + " fichier non trouve")
        exitProgram()

def remove_directory(folder:str):
    try:
        os.path.isdir(folder)
        shutil.rmtree(folder)   
    except OSError:
        print("File handler: problème avec la suppression du repertoire")
        exitProgram()

def remove_file(file:str):
    try:
        os.path.isfile(file)
        os.remove(file)   
    except OSError:
        print("File handler: problème avec la suppression du fichier")
        exitProgram()

# Deplacer un repertoire
def move_directory(src_path:str, dest_path:str):
    try:
        #shutil.move(pathFile + myNewFolderName + '/' + 'IP2LOCATION-LITE-DB11.CSV', myPath + 'IP2LOCATION-LITE-DB11.CSV' )
        shutil.move(src_path, dest_path)
    except:
        print("File handler: probleme de deplacement de : " + src_path + " vers " + dest_path)
        exitProgram()

# Renommer une archive
def rename_directory(current_folder_name:str, new_folder_name:str):
    try:
        os.path.isdir(current_folder_name)
        os.rename(current_folder_name, new_folder_name)
    except:
        print("File handler: probleme de renomage de : " + current_folder_name + " en " + new_folder_name)
        exitProgram()

# Exraction d un fichier specifique depuis une archive Zip
def extract_a_specified_file_from_zip_archive(archive_path_file_name:str, fileName_to_extract:str, dest_extraction_path:str):
 
    with ZipFile(archive_path_file_name, mode="r") as zip_ref:
        try:            
            zip_ref.extract(fileName_to_extract, dest_extraction_path)
            zip_ref.close()

        except:
            print("File handler: probleme d'extraction de l'archive: " + archive_path_file_name)
            exitProgram()

# Verifier que la taille du fichier n est pas nulle
def check_sizeFileNotNull(path_and_file_name:str):
    if not os.path.isfile(path_and_file_name) and not os.path.getsize(path_and_file_name) > 0:
        print("File handler: le fichier : " + path_and_file_name + " presente une taille de : " + os.path.getsize(path_and_file_name))  
        exitProgram()

def move_file(src_path_file:str, dest_path_file:str):
    try:
        shutil.move(src_path_file, dest_path_file)
    except:
        print("File handler: le fichier " + src_path_file + " deplace vers : " + dest_path_file)


# Ecrire dans le fichier de persistance des logs enseigné par 
# l'argument au lancement de la ligne de commande
def write_file(fileNamePath: str, content: str):
    try:
        file = open(fileNamePath, "a")
        file.write(content + "\n")
        
    except OSError:
        print("File handler: Impossible decrire dans le fichier  " + fileNamePath)
        exitProgram()

# Lire un fichier texte
def read_file(filename:str):
    try:
        with open(filename, "r") as fileToRead:
            line = fileToRead.readline()

    except IOError:
        print("file_handler: impossible d'ouvrir le fichier pour la lecture: " + filename)
        exitProgram()   

    return line