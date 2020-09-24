# pip install elasticsearch
# es_handler
# Test avec ES 7.5, biento ES7.6

from log_generator.es_constants import index_template_name, index_mapping, index_name_pyloggen
from log_generator.es_constants import index_template_settings_1, index_template_settings_2, index_template_settings_3, index_template_settings_4
from log_generator.es_constants import pipeline_user_agent, user_agent_pipeline_name
from log_generator.logger_handler import logger_configurator, logLevel_Converter
from log_generator.exit_program import exitProgram
from log_generator.dateTime_handler import get_date_onlyDate_now
import elasticsearch, requests, json, logging
from elasticsearch import helpers
import time
from datetime import datetime


# logger du module
logger_configurator()
logger = logging.getLogger(__name__)

bulkToProcess = []

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
        if cHealth["status"] == "green" or cHealth["status"] == "yellow":
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
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es_cluster_nodeNumber = es.cluster.health()["number_of_nodes"]
        print("es_api: Cluster_number_of_nodes : " + str(es_cluster_nodeNumber) )
    
    except elasticsearch.ElasticsearchException:
        print("es_api: Cluster_Number_of_nodes : impossible de determiner le nombre de noeud")
        exitProgram()

    return es_cluster_nodeNumber

# Définir le nombre de shard / replica selon le nombre de noeuds
def es_setShardReplicaNumber(ip:str):
    nodeNumber = es_getNodeNumber(ip)
    if nodeNumber == 1:
        shardNumber = 1
        replicaNumber = 0
        template = index_template_settings_1
    elif nodeNumber == 2:
        shardNumber = 1
        replicaNumber = 1
        template = index_template_settings_2
    elif nodeNumber == 3:
        shardNumber = 2
        replicaNumber = 2
        template = index_template_settings_3
    elif nodeNumber > 3:
        shardNumber = 3
        replicaNumber = 2
        template = index_template_settings_4
    print("es_api: " + str(nodeNumber) + "_noeud(s) detecte => templateConf: " + str(shardNumber) + "_shard(s) & " + str(replicaNumber) + "_replica(s)" )

    return template

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

# Verifier que le template existe et en cree un
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
    index_template_settings = es_setShardReplicaNumber(ip)
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
        elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        
    except elasticsearch.ConnectionError:
        print("es_api: Index impossible de savoir si l index existe")


# Ajouter un index
def es_create_new_index(ip:str, index_name:str):
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.index(index_name,{"userAgent":"none","ip_address":'1.1.1.1'})
        if es.indices.exists(index_name):
            print("es_api: Index => " + index_name + " cree")
        else:
            print("es_api: Index non cree " + index_name)

    except elasticsearch.ElasticsearchException:
        print("es_api: probleme a la creationde l index")
        exitProgram()

# Ajout de document dans l index
def es_add_document(ip:str, payload,totalOfIdicesToSend:int, actualIndiceNumber:int):
    global bulkToProcess
    if totalOfIdicesToSend < 11:
        es_send_single_document(ip,payload)
    else:
        bulkToProcess.append(payload)
        print("es_api: Json injection to array")
        if len(bulkToProcess) == totalOfIdicesToSend:
            bulkProcess_State(totalOfIdicesToSend, actualIndiceNumber)
            es_add_document_to_buk(ip, convert_arrayToBulk(bulkToProcess))
            

def convert_arrayToBulk(bulkToProcess):
    jsonBulk:str = ""
    index_name = index_name_pyloggen + get_gen_date_index()
    for document in bulkToProcess:
        yield {
            "_index" : index_name,
            "_type" : "_doc",
            "_source" : document
        }
    
def es_send_single_document(ip:str, payload):
    index_name: str =  index_name_pyloggen + get_gen_date_index()
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        es.index(index_name, payload)
        logger.info("Document ajouté")
    except elasticsearch.ElasticsearchException:
        print("es_api: _docAdd_Single_doc: il y a un probleme lors de l ajout du document")      
        logger.error("propbleme lors de l'ajout du document")

def es_add_document_to_buk(ip:str, jsonBulkIter):
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        #es.index(index_name, payload)
        helpers.bulk(client=es,actions=jsonBulkIter)
        #es.bulk(jsonBulk)

    except elasticsearch.ElasticsearchException:
        print("es_api: _docAdd_Bulk_Doc: il y a un probleme lors de l ajout du document")      
        logger.error("Bulk probleme lors de l'ajout du document")

# recupere le nombre de shard d un index
def es_get_index_shard_number(ip:str):
    try:
        index_name_today:str = es_get_index_name_datenow() 
        es = elasticsearch.Elasticsearch([{'host':ip, 'port': 9200}])
        result = es.indices.get_settings(index_name_today)[index_name_today]['settings']['index']['number_of_shards']

    except elasticsearch.ElasticsearchException:
        print("es_api: _get_index_shard_number: nombre de shard non recupere")      
        logger.error("propbleme lors de la recuperation du nombre de shard de l index: ")
    return int(result)

def bulkProcess_State(totalOfIdicesToSend:int, actualIndiceNumber:int):
    return

# Recupere juste la date
def get_gen_date_index():
    return get_date_onlyDate_now()

# Retourne l index name du jour
def es_get_index_name_datenow():
    return index_name_pyloggen + get_gen_date_index()

# Compte le nombre de documents de l index fourni
def es_count_of_given_indexName(ip:str, given_IndexName:str):
    time.sleep(5)
    try:
        es = elasticsearch.Elasticsearch([{'host': ip,'port': 9200 }])
        myCount = es.count(index=given_IndexName)["count"]
        return myCount

    except elasticsearch.ElasticsearchException:
        print("es_api: _countDoc il y a un probleme lors du count de l'index " + given_IndexName) 