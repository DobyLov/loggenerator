""" user agent handler """

import os
from datetime import datetime, date
from random import randrange

# Verification de la presence du fichier
def ua_check_file_exist(ua_file_with_path:str):

    file_exist: bool = False  
    try:
        if os.path.exists(ua_file_with_path):
            file_exist: True
            print("Bdd file: user_agent ouverture du fichier : " + ua_file_with_path)

    except OSError:
        print("Bdd file: user_agent " + ua_file_with_path + " not found.")
        exitProgram()

    return file_exist
        

# Compter le nombre de ligne du fichier
def ua_count_file_row_number(my_path:str, ua_file:str):

    try:
        print("Bdd file: user_agent nombre de lignes dans le fichier : " + str(len( open(my_path + ua_file).readlines())   ))
        return int(len( open(my_path + ua_file).readlines())   ) 

    except IOError:
        print("Bdd file: user_agent impossible d ouvrir le fichier " + my_path + ua_file)
        exitProgram()
    

# choisir un nombre entre 0 et le nombre fourni par la variable number_of_row
def ua_get_random_number(number_of_rows:int):
    return randrange(1, number_of_rows)

# Retoruner l user agent
def ua_get_user_agent(my_Path:str, my_File:str, number_of_rows:int):
    number_of_rows = ua_get_random_number(number_of_rows)
    return ua_read_userAgent_line_from_file_and_givenNumber(my_Path, my_File, number_of_rows )

# Renvoyer l user agent en fonction du nombre
def ua_read_userAgent_line_from_file_and_givenNumber(my_path:str, my_file:str, given_number:int):

    try:
        with open(my_path + my_file) as my_io_file:
            for lineNumber, line in enumerate(my_io_file):
                if lineNumber == given_number:
                    return line

    except IOError:
        print("Bdd file: user_agent impossible d ouvrir le fichier " + my_path+my_file)
        exitProgram()
    

# Retourne la date et l heure
def get_dateNow():
    
    my_dateTimeNow = datetime.now()
    my_years = str(my_dateTimeNow.year)
    my_months = addZero(str(my_dateTimeNow.month))
    my_days = addZero(str(my_dateTimeNow.day))
    my_hours = addZero(str(my_dateTimeNow.hour))
    my_minutes = addZero(str(my_dateTimeNow.minute))
    my_seconds = addZero(str(my_dateTimeNow.second))
    my_concatened_dateNow: str = my_years + "-" + my_months + "-" + my_days + " " + my_hours + ":" + my_minutes + ":" + my_seconds

    return my_concatened_dateNow

# Ajoute 0 devant les unitees ( jours et mois )
def addZero(mystr: str):

    if len(mystr) == 1:
        zeroBeforeValue = mystr.zfill(2)
    else:
        zeroBeforeValue = mystr
    
    return zeroBeforeValue

# sortir du programme
def exitProgram():
    import sys
    print("Sortie du programme : " + get_dateNow())
    sys.exit()