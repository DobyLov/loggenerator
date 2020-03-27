
"""
#!/usr/bin/env python3.6
#!/usr/bin/env python3
"""

"""log generator.

A command line application to generate random log.

"""

#from log_generator.testA import bonjour, message
from log_generator.network_handler import pingHost
from log_generator.operating_system_handler import get_platform, get_osVersion, get_osRelease 
from log_generator.es_handler import es_getSrvResponse, es_getSrvVersion, es_getSrvColorStatus, es_getNodeNumber, es_setShardReplicaNumber
from log_generator.es_handler import es_check_existing_template
from log_generator.es_handler import es_check_existing_index, es_create_new_index, es_add_document
from log_generator.es_handler import es_check_existing_pipeline
from log_generator.ua_handler import ua_check_file_exist, ua_get_user_agent, ua_count_file_row_number
from argparse import ArgumentParser
from random import choice as randchoice
import json, ipaddress, uuid
import sys, requests, random, time
from requests.exceptions import HTTPError
from urllib import parse as stringParserToUrl
from os import path
import shutil  # a tester glob
from zipfile import ZipFile
from datetime import datetime, date
from .words_constants import HASHTAGS, MESSAGE_TWEET, ADJECTIVES, NOUNS

# Variables

# Path
myPath = "./log_generator/"

# Csv
myCsvFile = "IP2LOCATION-LITE-DB11.CSV"
myZipFile = "IP2LOCATION-LITE-DB11.CSV.ZIP"
lineNumber:int = 0
myArray = []

# User Agent
ua_file = "list_of_comon_user_agent.txt"
print("ua_path " + myPath + ua_file)

errorCountIndice: int = 0

# http server
http_pathLogErrorFile = "./error_httpLogFile.txt"

# Verifie si le fichier de base donnee des userAgent existe 
def check_ua_file_exist(myPath:str, ua_file:str):
    ua_check_file_exist(myPath + ua_file)

# ua_
def recupere_nombre_ligne_ua_file(myPath, ua_file):
    global ua_number_of_lines_from_file 
    ua_number_of_lines_from_file = ua_count_file_row_number(myPath, ua_file)


# Gestion du fichier d'importation des données
def check_bddFile(myPath: str, myZipFile: str, myCsvFile: str):
    print("Verification si le fichier bdd est present au format Csv")
    if checkCsvFileExist(myPath, myCsvFile) == True:
        print(myPath +  myCsvFile + " present")
    else: 
        if checkZipFileExist(myPath,myZipFile) == True:
            print("Fichier non présent")
            unzipFile(myPath, myZipFile, myCsvFile)
        else:
            print("Fichier zip Bdd pour extraction absent")
            exitProgram()

# verification de la taille du fichier
def check_sizeFileNotNull(myPath, myCsvFile):
    import os
    myFile = myPath + '' + myCsvFile
    print("Verification de la taille du fichier : " + myCsvFile)
    if os.path.isfile(myFile) and os.path.getsize(myFile) > 0:
        print("Le fichier : " + myCsvFile + " presente une taille de : " + os.path.getsize(myFile))  
    else:
        if os.path.getsize(myFile) == 0:
            print("Le fichier : " + myCsvFile + " est de taille nulle")
            exitProgram()


# Map CSV to ARRAY : return an Array and a number of lines
def map_csv2array(myPath: str, myCsvFile: str):
    myFilePath:str = myPath + myCsvFile
    global lineNumber
    global myArray
    if len(myArray) == 0:
        with open(myFilePath, "r") as fileToRead:
            print ("Ouverture du fichier : " + myFilePath)
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
            print (str(ctn) + " lignes comptée depuis le fichier : " + myFilePath)
    return myArray

def check_arguments(args: dict):

    print("________________________________")
    print("")
    print("-  Script générateur de logz   -")
    print("________________________________")
    print("")

    print("Script debuté le " + get_dateNow())

    #if args["min_size"] >= args["max_size"]:
    #    raise ValueError("Max size must be greater than min size")
    #if args["min_size"] > 14 or args["max_size"] < 8:
    #    raise ValueError("Word range must be between 3 and 14")

    if args["num"] > 10000000:
        raise ValueError("Can't generate more than 1000 logz")
    
    #if args["addrip"]:
    #    ipaddr = "localhost"

    # Charge le fichier de bdd d adresse ip
    check_bddFile(myPath, myZipFile, myCsvFile)
    # map bdd ip file into an array
    map_csv2array(myPath, myCsvFile)
    # verifier que le fichier userAgent existe
    check_ua_file_exist(myPath, ua_file)
    # recupere le nombre total de ligne dans le fichier ua
    recupere_nombre_ligne_ua_file( myPath, ua_file)


    if args["esapiip"] != "":
        print(" ")
        print("---------------")
        print("- Elastic Api -")
        print("---------------")
        pingHost(args["esapiip"])
        es_getSrvResponse(args["esapiip"])
        es_getSrvColorStatus(args["esapiip"])
        es_getSrvVersion(args["esapiip"])
        es_getNodeNumber(args["esapiip"])
        es_setShardReplicaNumber()
        es_check_existing_pipeline(args["esapiip"])
        es_check_existing_template(args["esapiip"])
        #es_check_existing_index(args["esapiip"])


# Get the tweet for log and url format (cURL)
def get_log():
    
    global ip_fake, messagetweet, uuid, age

    name: str = get_name()
    messagetweet = randchoice(MESSAGE_TWEET)
    row = get_randomRow(myArray)
    ip_fake = get_fakeIp(row)
    get_infoRowFromGroup(row)
    hashTags, hashTagsArray = genHashtags()
    uu_id = get_uuid()
    age = get_age()
    dateNow = get_dateNow()
    userAgent = ua_get_user_agent(myPath, ua_file, ua_number_of_lines_from_file ) 
    # msg       
    singleLogToLogFile = ip_fake + " " + dateNow + " " + name + " " + hashTags + " " + '"' + messagetweet + '"' + " " + str(age) + " " + uu_id + " " + country_short + " " + country_long + " " + region + " " + town + " " + longitude + " " + latitude + " " + time_zone + " " + userAgent
    singleLogToUrl = stringParserToUrl.quote(ip_fake + " " + dateNow + " " + name + " " + hashTags + " " + messagetweet + " " + str(age) + " " + uu_id + " " + country_short + " " + country_long + " " + region + " " + town + " " + longitude + " " + latitude + " " + time_zone + " " + userAgent)
    
    singleLogToJson = json.dumps( 
        {
            "ip_address": ip_fake,
            "dateTime": dateNow,
            "user": name,
            "hasTags": hashTagsArray,
            "message_tweet": messagetweet,
            "age": age,
            "uuid": uu_id,
            "userAgent": userAgent,
            "country": {
                "location": {
                    "longitude": longitude,
                    "latitude": latitude },
                "country_short": country_short,
                "country_long": country_long,
                "region": region,
                "town": town,
                "time_zone": time_zone}
        } 
    )  
     
    
    #print(str(myJsonFormat))

    return singleLogToLogFile, singleLogToUrl, singleLogToJson

# Génère un pseudo nom avec @ en préfixe et avec ou sans underscore
def get_name():
    adjective = randchoice(ADJECTIVES)
    noun = randchoice(NOUNS)
    camel_case_adjective = " @" + adjective[0].upper() + adjective[1:]
    camel_case_noun = noun[0].upper() + noun[1:]
    underscores = randomUnderscore()
    if underscores:
        name: str = camel_case_adjective + camel_case_noun
    else:
        name: str = camel_case_adjective + "_" + camel_case_noun
    return name

# Retourne la date et l heure
def get_dateNow():
    
    my_dateTimeNow = datetime.now()
    my_years = str(my_dateTimeNow.year)
    my_months = addZero(str(my_dateTimeNow.month))
    my_days = addZero(str(my_dateTimeNow.day))
    my_hours = addZero(str(my_dateTimeNow.hour))
    my_minutes = addZero(str(my_dateTimeNow.minute))
    my_seconds = addZero(str(my_dateTimeNow.second))
    #tz = str(my_dateTimeNow.isoformat() )
    my_concatened_dateNow: str = my_years + "-" + my_months + "-" + my_days + "T" + my_hours + ":" + my_minutes + ":" + my_seconds

    return my_concatened_dateNow
    #return tz

# Ajoute 0 devant les unitees ( jours et mois )
def addZero(mystr: str):

    if len(mystr) == 1:
        zeroBeforeValue = mystr.zfill(2)
    else:
        zeroBeforeValue = mystr
    
    return zeroBeforeValue

def main(**kwargs):
    """Main."""
    # parse command line arguments
    parser = ArgumentParser(description="Generate log.")
    
    parser.add_argument("--num", metavar="NUMBER", type=int,
                        default=1, help="change number of logs generated")
    parser.add_argument("--no_print", default=False, action="store_true",
                        help="prevent printing logss to terminal")
    parser.add_argument("--fname", metavar="FILE NAME", default="",
                        help="save output in a text file")
    parser.add_argument("--speed_gen", metavar="NUMBER", type=int,
                    default=1, help="set speed log generation")
    parser.add_argument("--errlog", metavar="FILE NAME", default="",
                        help="save output log text file")
    parser.add_argument("--infinite", default=False, action="store_true",
                        help="infinit log")
    parser.add_argument("--webip", default="", type=str,
                        help="target Ip to send logz")
    parser.add_argument("--no_pause", default=False, action="store_true",
                        help="prevent pause printing logs to terminal")
    parser.add_argument("--esapiip", default="", type=str,
                    help="elastic api ip address")
    parser.add_argument("--bulknum", metavar="NUMBER", type=int,
                    default=1, help="number of indices to send es api bulk")

    # get args
    if "args" in kwargs:
        args = kwargs["args"]
    else:
        args = vars(parser.parse_args())
    try:
        check_arguments(args)
    except ValueError as error:
        print("Error: " + str(error))
        exit(1)

    # Read args and generate logz
    for _ in range(args["num"]): 

        output_text, output_text_url, output_json = get_log()
        if (args == "" or args["num"] == 1) and args["infinite"] == False:
            print(output_text)

        elif args["num"] > 1:
            if not args["no_pause"]:
                randomPause(args["speed_gen"])
            if not args["no_print"]:
                print(output_text)
            if args["fname"] != "":
                log2File(output_text, args["fname"])
            if args["esapiip"] != "":
                print("esapiip detectee")
                es_add_document(args["esapiip"], output_json)
            if args["webip"] != "":
                print("addrip detectee")
                postToHAProxy(args["webip"], output_text_url)

    if args["infinite"] == True:

        while True:
            output_text, output_text_url, output_json = get_log()
            if not args["no_pause"]:
                randomPause(args["speed_gen"])
            if not args["no_print"]:
                print(output_text)
            if args["fname"] != "":
                log2File(output_text, args["fname"])
            if args["webip"] != "":
                postToHAProxy(args["webip"], output_text_url)
            if args["esapiip"] != "":
                es_add_document(args["esapiip"], output_json)


if __name__ == "__main__":
    main()
 
# Générer les log au format json
def get_json():
    myJson:str = ""
    return myJson

# Age aléatoire entre 18 et 99 
def get_age():
    age = random.randint(18,99)
    return age

# UuidGen
def get_uuid():
    return str(uuid.uuid4())

# Random pour des pauses en millisecondes puis en secondes 
def randomPause(pauseLevel:int):
    # Lent x docs / min
    if pauseLevel <= 1:
        timemillis = [0, 0, 0, 0.0001, 0.0002, 0.0003, 0, 0.0004, 0.0005, 0.006, 0.0007, 0.008, 0.0009, 0.010, 0.50, 0.100, 0.200, 0.400, 0.500, 0.600, 0.700, 0.800, 0.900, 1, 0, 3, 0, 4, 5, 6, 7, 8, 9, 10]
    # Moyen x docs / min
    elif pauseLevel > 1 and pauseLevel <= 2: 
        timemillis = [0, 0, 0, 0.0001, 0.0002, 0.0003, 0, 0.0004, .0005, 0, 0.0007, 0.0009, 0, 0.100, 0.200, 0, 0.400, 0.5, 0, 1, 0, 3, 0]
    # Rapide x docs / min
    elif pauseLevel >= 3:
        timemillis = [0, 0, 0, 0.0001, 0.0002, 0.0003, 0, 0.0004, 0.0005, 0.006, 0.0007, 0, 0.008, 0.0009, 0, 0.010, 0.50, 0.100, 0.200, 0, 0.500, 0.600, 1, 0]
    
    secs = randchoice(timemillis)
    makePause(secs)
    #return

# Réalise une pause de x secondes
def makePause(pauseTime):
    time.sleep(pauseTime)
    #return

# Random pour mettre un underscore dans le Tweeter username
def randomUnderscore():
    boulboul: bool = random.choice([True, False])
    return boulboul

# Random pour le nombre de #HASTAGS 1, 2, 3, 4, 5
def randomNbHashtags():
    nbhashtags = random.randrange(1, 5, 1)
    return nbhashtags

# Générer la string de 1 ou x Hashtag(s)
def genHashtags():
    hashtagsArray = []
    nbHastag = randomNbHashtags()
    hashTagStr = randomHashtags()
    hashtagsArray.append(hashTagStr)
    for i in range(nbHastag):
        if i > 1: 
            addSeparator:str = ('"' + ", " + '"')
            addAshtag = randomHashtags()
            hashTagStr = hashTagStr + addSeparator + addAshtag
            hashtagsArray.append(addAshtag)

    return str('["' + hashTagStr + '"]'), hashtagsArray

# Random sur les Hashtags
def randomHashtags():
    hashtag = randchoice(HASHTAGS)
    return hashtag

# Ecrire dans le fichier renseigné par 
# l'argument au lancement de la ligne de commande
def log2File(output_text: str, filePath: str):
    try:
        file = open(filePath, "a")
        file.write(output_text + "\n")
    except OSError as err:
        print("OS error: {0}".format(err))

# Send To HA Proxy
def postToHAProxy(ip:str, logz:str):

    if ip != "" or ip == "localhost":
        fulladdress = "http://" + str(ip) + "/logz/" + logz
        try:
            requests.get(fulladdress)
        except Exception as err:
            writeHttpErrorLog("Request fail : " + fulladdress)
            writeHttpErrorLog(f'err : {err}') # Python 3.6


# Write log file from http get error
def writeHttpErrorLog(message :str):
    global http_pathLogErrorFile
    fullErrorMsg = str(datetime.now()) + "\t" + str(message)
    print()
    print("Erreur : La requete http n'a pas aboutie.")
    print("Erreur passée dans le Logfile : " + http_pathLogErrorFile)
    print()
    try:
        file = open(http_pathLogErrorFile, "a")
        file.write(fullErrorMsg + "\n")
    except OSError as err:
        print("OS error: {0}".format(err))

# Get a random row
def get_randomRow(myArray):
    global row
    row = get_rowFromIdArray(get_randomNumber(myArray))
    return row
    
# Get Row from a given number
def get_rowFromIdArray(lineNumber: int):
    row = myArray[lineNumber]
    return row

# Get a random number from lenArrayCSV rangesize
def get_randomNumber(myArray):
    minusMyArray: int = len(myArray) - 1
    randomNumFromLenArray:int = random.randrange(1, minusMyArray)
    return randomNumFromLenArray

# filter the given row an extract info from groupto an array
# regex group id
# 1, 2, 3 , 4, 5, 6, 7, 8, 9, 10
# ipRangeStart, ipRangeEnd, countryShort, countryLong,region, ville, long, lat, chépo, timezone
# "3287672320","3287672575","DE","Germany","Hessen","Frankfurt am Main","50.115520","8.684170","65931","+01:00"
def row_filter_forIpRange(row: str):
    global errorCountIndice
    #print("pipo : " + row)
    import re
    arrayOfRangeIpAdress = []
    # regex pour filtrer la plage d ip
    rowFiltred: str = re.search(r'\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\"', row)

    # Cette partie de code est devenue inutile, plus d 'erreure possible
    # La clause if / else peut etre supprimmée et conserver l append de la valeur des groupes 1 et 2 
    if rowFiltred:
        arrayOfRangeIpAdress.append(int(rowFiltred.group(1)))
        arrayOfRangeIpAdress.append(int(rowFiltred.group(2)))
    else:
        print("[erreur " + str(errorCountIndice) + "]" + " problème d'extraction car la ligne est vide :()")
        if not row:
            arrayOfRangeIpAdress.append(34603520)
            arrayOfRangeIpAdress.append(34604031)
            print("[erreur " + str(errorCountIndice) + "]" + " plage imposée : " + 
            str(arrayOfRangeIpAdress[0]) + "-" + str(arrayOfRangeIpAdress[1]))
            print("[erreur " + str(errorCountIndice) + "]" + " le script continue normalement")
            errorCountIndice += 1
    return arrayOfRangeIpAdress

# Retourne l information en focntion du numéro de groupe demandedu regex 
# regex group id
# 1, 2, 3 , 4, 5, 6, 7, 8, 9, 10
# ipRangeStart, ipRangeEnd, countryShort, countryLong,region, ville, long, lat, chépo, timezone
# "3287672320","3287672575","DE","Germany","Hessen","Frankfurt am Main","50.115520","8.684170","65931","+01:00"
def get_infoFromRowAndGroupNumber(row: str, groupeNumber: int):
    import re
    row_grouped: str = re.search(r'\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\"', row)
    groupInfo: str = row_grouped.group(groupeNumber)
    return groupInfo

# Return an random string ipAdress from the range given by an array with start/end values
def get_randomIpAdressFromRange(arrayOfIpAddress):
    random_Ip = random.randrange(int(arrayOfIpAddress[0]),int(arrayOfIpAddress[1]))
    return random_Ip

# Recupere une adresse ip aléatoire 
def get_fakeIp(row: str):
    ipRangeFrom_row_filtered = []
    ipRangeFrom_row_filtered = row_filter_forIpRange(row)
    ipAddr = get_randomIpAdressFromRange(ipRangeFrom_row_filtered)
    convertedIp:str = ip_converter(ipAddr)
    return convertedIp

# Convertisseur ip integer en string ip
def ip_converter(intIpAddress):    
    ip:str = str(ipaddress.ip_address(intIpAddress))
    return ip

# Extraire l'information de la 'row' en fonction de la regex via position de groupe 
# regex group id
# 1, 2, 3 , 4, 5, 6, 7, 8, 9, 10
# ipRangeStart, ipRangeEnd, countryShort, countryLong,region, ville, long, lat, chépo, timezone
# "3287672320","3287672575","DE","Germany","Hessen","Frankfurt am Main","50.115520","8.684170","65931","+01:00"
# L'id_groupe doit etre superieur à 2 car les id_groupe 1 et 2 sont reservés pour le calcul de la plage d'adresse IP 
def get_infoRowFromGroup(row: str):
    import re
    rowFiltred: str = re.search(r'\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\"', row)
    global country_short, country_long, region, town, longitude, latitude, chepo, time_zone
    country_short = rowFiltred.group(3)
    country_long = rowFiltred.group(4)
    region = rowFiltred.group(5)
    town = rowFiltred.group(6)
    longitude = rowFiltred.group(7)
    latitude = rowFiltred.group(8)
    chepo = rowFiltred.group(9)
    time_zone = rowFiltred.group(10)

# Verification si le fichier existe
def checkZipFileExist(myPath: str, myZipFile: str):
    myPathFile: str = myPath + '' + myZipFile
    fichierPresent: bool = False
    print("Verification si le fichier Zip fourni en paramètre existe")
    #print("Chemin fourni : " + myZipFile)
    if path.exists(myPathFile):
        print(myZipFile + " trouvé")
        fichierPresent = True
    else:
        print(myZipFile + " Non trouvé")
        fichierPresent = False
    return fichierPresent

def checkCsvFileExist(myPath:str, myCsvFile:str):
    myPathFile: str = myPath + '' + myCsvFile
    fichierPresent: bool = False
    print("Verification si le fichier Csv fourni en paramètre existe")
    #print("Chemin fourni : " + myPath)
    if path.exists(myPathFile):
        print(myZipFile + " trouvé")
        fichierPresent = True
    else:
        print(myZipFile + " Non trouvé")
        fichierPresent = False
    return fichierPresent

def unzipFile(pathFile: str, myZipFile: str, myCsvFile: str):
    import os
    myPathZipFile: str = pathFile + '' + myZipFile 
    myPathCsvFile: str = pathFile + '' + myCsvFile
    myNewFolderName: str = "IP2LOCATION"
    with ZipFile(myPathZipFile, mode="r") as zip_ref:
        try:
            print("Extraction du fichier : " + myZipFile)
            zip_ref.extract('IP2LOCATION-LITE-DB11.CSV',myPathCsvFile)            
            print("L'extraction s'est bien déroulée")
            zip_ref.close()
        except:
            print("Il y a eu un problème avec l'extraction de l'archive")
            exitProgram()
    try:
        print("Renomer le repertoire")
        if os.path.isdir(myPathCsvFile):
            os.rename(myPathCsvFile, myPath + '/' + myNewFolderName)
            print("le renommage s est bien déroulé")
        else:
            print("Il y a eu une erreur au renomage du repertoire")
    except:
        print("Il y a eu une erreur au renomage du repertoire")
    try:
        print("Déplacement du fichier : " + myCsvFile)
        shutil.move(pathFile + myNewFolderName + '/' + 'IP2LOCATION-LITE-DB11.CSV', myPath + 'IP2LOCATION-LITE-DB11.CSV' )
    except:
        print('Il y a eu un problème avaec la copie du fichier : ' + myCsvFile)
    try:
        print("Suppression du repertoire" + myNewFolderName)
        if os.path.isdir(myPath + myNewFolderName):
            shutil.rmtree(myPath + myNewFolderName)
            print("la suppression s est bien deroulee")
        else:
            print(myPath + '/' + myNewFolderName + " n est pas un repertoire")    
    except:
        print("Il y a eu un problème avec la suppression du repertoire")

# sortir du programme
def exitProgram():
    import sys
    print("Sortie du programme : " + get_dateNow())
    sys.exit()