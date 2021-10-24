# kafka handler

#from confluent_kafka import Producer
#import socket
from kafka import BrokerConnection,KafkaProducer,KafkaClient
from datetime import datetime
import json
from log_generator.network_handler import pingHost

kfkPort = "9092"


def kf_produce_msg(kfkipbroker, kfkTopic, kfkMsg):
    check_kfk_aviability(kfkipbroker, kfkTopic)
    sendKfkMsg(kfkipbroker, kfkTopic, kfkMsg)

def check_kfk_aviability(kfkipbroker, kfkTopic):
    pingHost(kfkipbroker)
    #check_kfk_service(kfkipbroker,kfkPort)
    

def sendKfkMsg(kfkipbroker, kfkTopic, kfkMsg):
    producer = KafkaProducer(bootstrap_servers=[kfkipbroker+":" +kfkPort])
    #value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(kfkTopic,kfkMsg.encode('utf-8'))


def check_kfk_service(kfkIpBroker, kfkPort):
    consumer = KafkaClient(kfkIpBroker,kfkPort)
    if not consumer.bootstrap_connected():
        print("kfk : Broker_" + kfkIpBroker + " service unaviable")
        exitProgram()
    
# Retourne la date et l heure
def get_dateNow():
    dateNow: str = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + " " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)
    return dateNow

# sortir du programme
def exitProgram():
    import sys
    print("Exit script : " + get_dateNow() )
    sys.exit()



