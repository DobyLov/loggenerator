""" Generateur de logz """
"""
#from log_generator.logz_handler
from . import myPath, ua_number_of_lines_from_file, ua_file, myArray
from log_generator.ip_handler import get_randomRow
from log_generator.ip_handler import latitude, longitude, country_long, country_short, region, town, time_zone
from log_generator.ip_handler import get_fakeIp
from log_generator.ip_handler import get_infoRowFromGroup
from log_generator.ua_handler import ua_get_user_agent
from log_generator.user_handler import get_age, get_uuid
from log_generator.dateTime_handler import get_dateNow

from urllib import parse as stringParserToUrl
from random import choice as randchoice
import json, random
"""
#from random import randrange
import random, json
from random import choice as randchoice
from urllib import parse as stringParserToUrl
from .words_constants import MESSAGE_TWEET
from log_generator.hashTag_handler import gen_Hashtags
from log_generator.dateTime_handler import get_dateNow
from log_generator.user_handler import get_name, get_age, get_uuid
from log_generator.ua_handler import ua_get_user_agent
from log_generator.ip_handler import get_randomRow, get_fakeIp, get_location_from_IP_Row

# Get the tweet for log and url format (cURL)
#def get_log():   
def get_log(myIPArray:[], myUAArray:[]): 
    #global ip_fake, messagetweet, uuid, age
    name = get_name()
    messagetweet = randchoice(MESSAGE_TWEET)
    row = get_randomRow(myIPArray)
    ip_fake = get_fakeIp(row)
    country_short, country_long, region, town, longitude, latitude, chepo, time_zone = get_location_from_IP_Row(row)
    #get_infoRowFromGroup(row)
    hashTags, hashTagsArray = gen_Hashtags()
    uu_id = get_uuid()
    age = get_age()
    dateNow = get_dateNow()
    userAgent = ua_get_user_agent(myUAArray)

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
    
    return singleLogToLogFile, singleLogToUrl, singleLogToJson