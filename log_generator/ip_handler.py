""" ip generateur """

from log_generator.exit_program import exitProgram
import ipaddress, random

# Get a random row
def get_randomRow(myIPArray):
    array_size = get_array_size(myIPArray)
    row = get_rowFromIdArray(myIPArray, get_randomNumber(array_size))
    return row

# Retourne la taille du tableau
def get_array_size(myArray):
    minusMyArray: int = len(myArray) - 1
    return minusMyArray

# Get a random number from lenArrayCSV rangesize
def get_randomNumber(number:int):
    return random.randrange(1, number)

# Get Row from a given number
def get_rowFromIdArray(myArray:[], lineNumber: int):
    row = myArray[lineNumber]
    return row



# filter the given row an extract info from groupto an array
# regex group id
# 1, 2, 3 , 4, 5, 6, 7, 8, 9, 10
# ipRangeStart, ipRangeEnd, countryShort, countryLong,region, ville, long, lat, chépo, timezone
# "3287672320","3287672575","DE","Germany","Hessen","Frankfurt am Main","50.115520","8.684170","65931","+01:00"
def row_filter_forIpRange(row: str):
    #global errorCountIndice
    errorCountIndice = 0 # peut etre supprimé
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
def get_location_from_IP_Row(row: str):
    import re
    rowFiltred: str = re.search(r'\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\"', row)
    #global country_short, country_long, region, town, longitude, latitude, chepo, time_zone
    country_short = rowFiltred.group(3)
    country_long = rowFiltred.group(4)
    region = rowFiltred.group(5)
    town = rowFiltred.group(6)
    longitude = rowFiltred.group(7)
    latitude = rowFiltred.group(8)
    chepo = rowFiltred.group(9)
    time_zone = rowFiltred.group(10)

    return country_short, country_long, region, town, longitude, latitude, chepo, time_zone


# Map CSV to ARRAY : return an Array and a number of lines
def map_csv2array(my_path_file_name:str):
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