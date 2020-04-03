""" user agent handler """

import os
from log_generator.dateTime_handler import get_dateNow
from log_generator.exit_program import exitProgram
from datetime import datetime, date
from random import randrange

# Retoruner l user agent
def ua_get_user_agent(myUAArray):
    arraySize = ua_get_arrayLength(myUAArray)
    randomNumber = get_random_number(arraySize)
    return ua_userAgent_from_givenNumber(myUAArray, randomNumber)

# Map CSV to ARRAY : return an Array and a number of lines
def map_ua_csv2array(my_path_file_name:str):
    try:
        with open(my_path_file_name, "r") as fileToRead:
            line = fileToRead.readline()
            ctn = 1
            myArray = []
            while line:
                line = fileToRead.readline()
                try:                
                    myArray.append(line)
                    ctn += 1
                except BufferError:
                    print("error: " + BufferError)
            print("Bdd handler: " + str(ctn) + " lignes comptée depuis le fichier : " + my_path_file_name)
        return myArray

    except IOError:
        print("Bdd hendler: impossible de mapper daas le tableau le fichier " + my_path_file_name)
        exitProgram()

# Retourne la taille de l Array
def ua_get_arrayLength(myUAArray):
    return len(myUAArray) - 1

# choisir un nombre entre 0 et le nombre fourni par la variable number_of_row
def get_random_number(number:int):
    return randrange(1, number)

# Retourne la ligne correspondante au numero demandé
def ua_userAgent_from_givenNumber(myUAArray:[], givenNumber: int):
    return myUAArray[givenNumber]


    