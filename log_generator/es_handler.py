# pip install elasticsearch
# es_handler
# Test avec ES 7.5

from log_generator.es_constants import index_template_settings, index_template_name, index_mapping, index_name_pyloggen
from log_generator.es_constants import pipeline_user_agent, user_agent_pipeline_name
#from elasticsearch import Elasticsearch, exceptions 
import elasticsearch
from datetime import datetime
import requests
import json


# Vérifier si le serveur repond
def es_getSrvResponse(ip:str):

    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        if not es.ping():
            print("es_api: " + ip + " ne repond pas")

    except elasticsearch.ConnectionError:
        print("es_api: " + ip + " ne repond pas")
        exitProgram()

# recupérér la version de ES
def es_getSrvVersion(ip:str):    
    
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        print("es_api: Cluster version: " + str( es.info()['version'].get("number") ) )

    except elasticsearch.ConnectionError:
        print("es_api: " + ip + " ne repond pas")
        exitProgram()
    

# Vérifier que le serveur est a green
def es_getSrvColorStatus(ip:str):    
    
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        cHealth = es.cluster.health()
        if cHealth["status"] == "green":
            print("es_api: Cluster_color: " + str(cHealth["status"]))
        
        else:
            print("es_api: Attention Cluster_color: " + str(cHealth["status"]))
            exitProgram()

    except elasticsearch.ElasticsearchException:
        print("es_api : " + ip + " ne repond pas")
        exitProgram()

# Attendre que le serveur renvoie le status code 200
def es_waitSrvReady(ip:str):
    res = requests.get("http://" + ip + ":9200")
    while res.status_code != 200:
        res = requests.get("http://" + ip + ":9200")

# Recuperer le nombre de noeud du cluster
def es_getNodeNumber(ip:str):

    global es_cluster_nodeNumber
    es_cluster_nodeNumber = 1  
    
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es_cluster_nodeNumber = es.cluster.health()["number_of_nodes"]
        print("es_api: Cluster_number_of_nodes : " + str(es_cluster_nodeNumber) )

    except elasticsearch.ElasticsearchException:
        print("es_api: Cluster_Number_of_nodes : impossible de determiner le nombre de noeud")
        exitProgram()

# Définir le nombre de shard / replica selon le nombre de noeuds
# 1 noeud => 1 shard 0 replicas
# 2 noeuds => 1 shard 1 replicat
# 3 noeuds => 2 shards 1 replicat
# 4 et plus => 2 shards 2 repicas
def es_setShardReplicaNumber():

    global shardNumber, replicaNumber
    shardNumber = 0 
    replicaNumber = 0
    if es_cluster_nodeNumber == 1:
        shardNumber = 1
        replicaNumber = 0
    elif es_cluster_nodeNumber == 2:
        shardNumber = 1
        replicaNumber = 1
    elif es_cluster_nodeNumber == 3:
        shardNumber = 2
        replicaNumber = 1
    elif es_cluster_nodeNumber > 3:
        shardNumber = 3
        replicaNumber = 2

    print("es_api: " + str(es_cluster_nodeNumber) + "_noeud(s) detecte => templateConf: " + str(shardNumber) + "_shard(s) & " + str(replicaNumber) + "_replica(s)" )



# Verifier que le Pipeline existe
def es_check_existing_pipeline(ip:str):

    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.ingest.get_pipeline(user_agent_pipeline_name)

    except elasticsearch.ElasticsearchException:
        print("es_api: Pipeline => " + user_agent_pipeline_name + " non trouve.")
        es_create_new_pipeline(ip)


# Creation du pipeline
def es_create_new_pipeline(ip:str):

    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.ingest.put_pipeline(user_agent_pipeline_name, pipeline_user_agent)
        
        if es.ingest.get_pipeline(user_agent_pipeline_name) :
            print("es_api: Pipeline cree => " + user_agent_pipeline_name)

    except elasticsearch.ElasticsearchException:            
        print("es_api: Pipeline : il y eu un problème a la creation du pipeline")
        exitProgram()

# Verifier que le template existe
def es_check_existing_template(ip:str):
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        if not es.indices.exists_template(index_template_name):
            print("es_api: Template: " + index_template_name + " non trouve.")
            es_create_new_template(ip)

    except elasticsearch.ElasticsearchException:
        print("es_api: Template impossible de savoir si le template existe")
        exitProgram()

# Creation de template
def es_create_new_template(ip:str):

    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.indices.put_template(index_template_name, index_template_settings)
        #es_waitSrvReady(ip)
        if es.indices.exists_template(index_template_name):
            print("es_api: Template cree => " + index_template_name)

    except elasticsearch.ElasticsearchException:            
        #print("es_Api: " + ip + " status code : " + str(res.status_code))
        print("es_api: il y eu un roblème a la creation du template")
        exitProgram()


# Verifier si l index existe
def es_check_existing_index(ip:str):

    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        index_name: str = index_name_pyloggen + get_gen_date_index()
        #if not es.indices.exists(index_name):
            #es_create_new_index(ip, index_name)
        
    except elasticsearch.ConnectionError:
        print("es_api: Index impossible de savoir si l index existe")


# Ajouter un index
def es_create_new_index(ip:str, index_name:str):

    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.index(index_name,{"userAgent":"none"})

        if es.indices.exists(index_name):
            print("es_api: Index => " + index_name + " cree")
        else:
            print("es_api: Index non cree " + index_name)

    except elasticsearch.ElasticsearchException:
        print("es_api: Index probleme a la creation")
        exitProgram()

# Ajoute un document dans l index
def es_add_document(ip:str, payload):
    
    index_name: str =  index_name_pyloggen + get_gen_date_index()
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.index(index_name, payload)
        

    except elasticsearch.ElasticsearchException:
        print("es_api: _docAdd il y a un probleme lors de l ajout du document")      


def get_gen_date_index():

    my_dateTimeNow = datetime.now()
    my_years = str(my_dateTimeNow.year)
    my_months = addZero(str(my_dateTimeNow.month))
    my_days = addZero(str(my_dateTimeNow.day))
    my_concatened_dateNow: str = my_years + "_" + my_months + "_" + my_days

    return my_concatened_dateNow

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