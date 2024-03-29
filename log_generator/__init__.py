
"""
#!/usr/bin/env python3.6
#!/usr/bin/env python3
"""

"""log generator.

A command line application to generate random log.

"""

from argparse import ArgumentParser
from log_generator.dateTime_handler import get_dateNow, calculat_elapsed_time, addZero
from log_generator.files_handler import file_exist_check, check_sizeFileNotNull, extract_a_specified_file_from_zip_archive, rename_directory, move_directory, remove_directory, file_exist_check_ifNot_exit, move_file
from log_generator.ip_handler import map_csv2array
from log_generator.files_logs_handler import log2File
from log_generator.logz_handler import get_log
from log_generator.network_handler import pingHost
from log_generator.es_handler import es_getSrvColorStatus, es_getSrvResponse, es_getSrvVersion, es_check_existing_pipeline, es_check_existing_template, es_get_index_name_datenow, es_count_of_given_indexName
from log_generator.ua_handler import map_ua_csv2array
from log_generator.es_handler import es_add_document, es_get_index_shard_number, es_create_new_index, es_check_ilm_policy_exist
from log_generator.webSrv_handler import web_post_document
from log_generator.logger_handler import logger_configurator, logLevel_Converter, check_exist_log_level, create_file_log_level, get_logLevel_from_file
from log_generator.kf_handler import kf_produce_msg
from random import choice as randchoice
import random, time, uuid, shutil, logging


# --------------------------------------
startScript = get_dateNow()
myPath = "./log_generator/"
myCsvFile = "IP2LOCATION-LITE-DB11.CSV"
myZipFile = "IP2LOCATION-LITE-DB11.CSV.ZIP"
lineNumber:int = 0
myUaFile = "list_of_comon_user_agent.txt"
error_log_file_path = "./error_httpLogFile.txt"
# les tableaux ip et userAgent sont initialisé ici
# Et sont porté a global dans la methode "check_argument"
myIPArray = []
myUAArray = []

logger = logging.getLogger(__name__)

def check_arguments(args: dict):
    logger_configurator()
    global logger
    logger = logging.getLogger(__name__)
    print("________________________________")
    print("")
    print("-  Script générateur de logz   -")
    print("________________________________")
    print("")
    print("Script debuté le " + get_dateNow())
    if args["num"] <= 0:
        raise ValueError("Je suis hors competence pour realiser votre demande irrationnelle ...\n Par example vous pourriez posez la question a siri ou Alexa :)")
    if args["num"] >= 500000:
        raise ValueError("Je suis desole mais je ne veux pas realiser une demande aussi grande\n passez en mode --infinite ou alors voyez ca avec le super calculateur de Google :)")
    
    print("------------------")
    print("- Chargement Bdd -")
    print("------------------")
    # Handle IP bdd file
    chrono_start_load_bdds = get_dateNow()
    if not file_exist_check(myPath + myCsvFile):
        # Check si le fichier Zip existe
        file_exist_check_ifNot_exit(myPath + myZipFile)
        extract_a_specified_file_from_zip_archive(myPath + myZipFile, myCsvFile, myPath + myCsvFile)
        rename_directory(myPath + myCsvFile, myPath + myCsvFile+".old")
        move_file(myPath + myCsvFile+".old/" + myCsvFile , myPath + myCsvFile)
        remove_directory(myPath + myCsvFile+".old")
    # map IP Bdd CSV file to array
    global myIPArray
    myIPArray = map_csv2array(myPath + myCsvFile)
    # Handle UA Bdd file
    if file_exist_check(myPath + myUaFile):
        global myUAArray
        myUAArray = map_ua_csv2array(myPath + myUaFile)
    else:
        print("Bdd handler: fichier non trouvé : " + myUaFile)
        exitProgram()
    #print("Bdd handler: temps pour charger les bases : " + str( calculat_elapsed_time( get_dateNow(), chrono_start_load_bdds ) ))

    if args["esapiip"] != "":
        print(" ")
        print("---------------")
        print("- Elastic Api -")
        print("---------------")
        pingHost(args["esapiip"])
        es_getSrvResponse(args["esapiip"])
        es_getSrvColorStatus(args["esapiip"])
        es_getSrvVersion(args["esapiip"])
        es_check_existing_pipeline(args["esapiip"])
        es_check_existing_template(args["esapiip"])
        es_check_ilm_policy_exist(args["esapiip"])
        es_create_new_index(args["esapiip"])

def main(**kwargs):
    """Main."""
    
    logger.info("Debut de script de generateur de logz")
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
    parser.add_argument("--kfkip", default="", type=str,
                    help="kafka broker ip")
    parser.add_argument("--kfktopic", default="", type=str,
                    help="specify a kafka topic")                    
    parser.add_argument("--loglvl", default="ERROR", type=str,
                    help="logger level (DEBUG, INFO, WARNING, ERROR)")

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

    # MEssage d information du script
    if args["esapiip"] != "":
        chrono_end_inject_docs = get_dateNow()  
        if args["infinite"] == True:
            print("es_api: Injection sans fin de documents, seul ctrl +c pour quitter.")
        else:
            print("es_api: Injection de(s) " + str(args["num"]) + " log(s)")  
        
        if args["num"] > 100:
            print ("es_api: Bulk_mode actif")
            print ("es_api: Génération en Ram des " + str(args["num"]) + " documents")
    
    if args["kfkip"] != "":
        chrono_end_inject_docs = get_dateNow()  
        if args["infinite"] == True:
            print("kfk_producer: Injection sans fin de documents, seul ctrl +c pour quitter.")
        else:
            print("kfk_producer: Injection de(s) " + str(args["num"]) + " log(s)") 
            
    for _ in range(args["num"]): 
        output_text, output_text_url, output_json = get_log(myIPArray, myUAArray)
        if (args == "" or args["num"] == 1) and args["infinite"] == False:
            if not args["no_pause"]:
                randomPause(args["speed_gen"])
            if not args["no_print"]:
                print(output_text)
            if args["fname"] != "":
                log2File(output_text, args["fname"])
            if args["esapiip"] != "":
                es_add_document(args["esapiip"], output_json)
            if args["webip"] != "":
                web_post_document(args["webip"], output_text_url, error_log_file_path)
            if args["kfkip"] !="":
                kf_produce_msg(args["kfkip"], args["kfktopic"], output_json)

        elif args["num"] > 1:
            if not args["no_pause"]:
                randomPause(args["speed_gen"])
            if not args["no_print"]:
                print(output_text)
            if args["fname"] != "":
                log2File(output_text, args["fname"])
            if args["esapiip"] != "":
                es_add_document(args["esapiip"], output_json, int(args["num"]), _)
            if args["webip"] != "":
                web_post_document(args["webip"], output_text_url, error_log_file_path)
            if args["kfkip"] !="":
                kf_produce_msg(args["kfkip"], args["kfktopic"], output_json)
    
    if args["infinite"] == True:
        while True:
            output_text, output_text_url, output_json = get_log(myIPArray, myUAArray)
            if not args["no_pause"]:
                randomPause(args["speed_gen"])
            if not args["no_print"]:
                print(output_text)
            if args["fname"] != "":
                log2File(output_text, args["fname"])
            if args["webip"] != "":
                web_post_document(args["webip"], output_text_url, error_log_file_path)
            if args["esapiip"] != "":
                #es_add_document(args["esapiip"], output_json)
                es_add_document(args["esapiip"], output_json, 1, 1)
            if args["kfkip"] !="":
                kf_produce_msg(args["kfkip"], args["kfktopic"], output_json)

    # -------------------------------------------------
    # Message de fin de script
    if args["esapiip"] != "":
        print("es_api: Temps total d'injection du/des " + str(args["num"]) + " doc(s) => " + str( calculat_elapsed_time(get_dateNow(), chrono_end_inject_docs)) )
        #print("es_api: index : " + es_get_index_name_datenow() + " count = " + str( es_count_of_given_indexName(args["esapiip"], es_get_index_name_datenow()) ) )


    if args["num"] >= 1:
        print("\n==============================================")
        print("Script terminé à : " + get_dateNow())
        print("Temps: " + str( calculat_elapsed_time(get_dateNow(), startScript) ) + " écoulé pour " + str(args["num"]) + " logs générés")
        print("Log level = " + get_logLevel_from_file() )
        print("==============================================")

if __name__ == "__main__":
    main()
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

# sortir du programme
def exitProgram():
    import sys
    print("Sortie du programme : " + get_dateNow())
    sys.exit()