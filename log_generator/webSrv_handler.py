""" Web server destination """

from log_generator.files_logs_handler import errorLog
from requests.exceptions import HTTPError
import requests

# Send To a web server
def web_post_document(ip:str, logz:str, errolog_path:str):

    if ip != "":
        fulladdress = "http://" + str(ip) + "/logz/" + logz
        try:
            requests.get(fulladdress)
        except Exception as err:
            errorLog("Request fail : " + fulladdress, errolog_path)
            errorLog(f'err : {err}',"") # Python 3.6
