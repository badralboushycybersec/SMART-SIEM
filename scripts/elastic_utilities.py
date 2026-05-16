#!/usr/bin/python3
try:    
    import config
    import pandas as pd
    from elasticsearch import Elasticsearch
    from elasticsearch import helpers
    from datetime import date
except Exception as e :
    print("Some Modules are Missing in Elastic_utilities.py {}".format(e))


def generator(df,index_name):
    # print("generator")
    # print(df["_id"][0])
    
    for index,row in df.iterrows():
        mail = False
        if(row["_source.rule.mail"] == 1):
            mail = True
        yield{
            '_index':index_name,
            '_type':'_doc',
            # '_id':row.get("_id",index),
            '_source':{
                'input_type':row.get("_source.input.type","log"),
                'agent_ip':row.get("_source.agent.ip"," "),
                "agent_name":row.get("_source.agent.ip"," "),
                "agent_id":row.get("_source.agent.id"," "),
                "manager_name":row.get("_source.manager.name"," "),
                'data_protocol':row.get('_source.data.protocol'," "),
                "data_srcip":row.get("_source.data.srcip"," "),
                'data_id':row.get('_source.data.id'," "),
                'data_url':row.get('_source.data.url'," "),
                'rule_firedtimes':row.get('_source.rule.firedtimes',1),
                'rule_mail':mail,
                'rule_level':row.get('_source.rule.level',1),
                'rule_description':row.get("_source.rule.description"," "),
                'rule_groups':row.get("_source.rule.groups"," "),
                'rule_id':row.get("_source.rule.id"," "),
                'location':row.get("_source.location"," "),
                'decoder_name':row.get("_source.decoder.name"," "),
                "id":row.get("_source.id"," "),
                "full_log":row.get("_source.full_log"," "),
                "timestamp":row.get("_source.timestamp","1111-1-11T1:11:1.1111Z"),
                "rule_pci_dss":row.get("_source.rule.pci_dss"," "),
                "rule_tsc":row.get("_source.rule.tsc"," "),
                "rule_nist_800_53":row.get("_source.rule.nist_800_53"," "),
                "rule_gdpr":row.get("_source.rule.gdpr"," "),
                "rule_mitre_id":row.get("_source.rule.mitre.id"," "),
                "rule_hipaa":row.get("_source.rule.hipaa"," "),
                "agent_description":row.get("_source.gent.description"," "),
                "rule_frequency":row.get("_source.rule.frequency"," "),
                "history_rule_firedtimes":row.get('history._source.rule.firedtimes'," "),
                'history_source_data_id_200':row.get('history._source.data.id.200'," "),
                'history_source_data_id_300':row.get('history._source.data.id.300'," "),
                'history_source_data_id_400':row.get('history._source.data.id.400'," "),
                'history_source_data_id_500':row.get('history._source.data.id.500'," "),

                'history_T1212':row.get('T1212'," "),
                'history_T1068':row.get('T1068'," "),
                'history_T1064':row.get('T1064'," "),
                'history_T1210':row.get('T1210'," "),
                'history_T1083':row.get('T1083'," "),
                'history_T1055':row.get('T1055'," "),
                'history_T1190':row.get('T1190'," "),


                "history_count_events":row.get("count_events",0),
                "output_1":row.get("output_1"," "),
                "output_2":row.get("output_2"," ")
                
            }
        }





def connect_elasticsearch():
    user=config.elasticsearch_user
    password = config.elasticsearch_password
    elasticsearch_ip=config.elasticsearch_ip
    elasticsearch_port = config.elasticsearch_port
    es = Elasticsearch(["https://" + user + ":"+password+"@"+elasticsearch_ip+":"+elasticsearch_port], verify_certs=False)
    if(es.ping()):
        return es
    return False




def read_from_elastic_search(ip,time,es):
    if(es==False):
        print("Can't connect to Elasticsearch trace: elastic_utilities -> read_from_elastic_search-> connect_elastic")
        return
    query  = config.query
    query["query"]["bool"]["filter"][2]["range"]["timestamp"]["lte"] = time
    query["query"]["bool"]["filter"][1]["match_phrase"]["data.srcip"] = ip
    first_qu = es.search(index="wazuh-alerts-*",body=query)
    dataframe = pd.json_normalize(first_qu["hits"]["hits"])
    return dataframe
    
    
    
def read_elasticrecord(id,es):
    if(es==False):
        print("Can't connect to Elasticsearch trace: elastic_utilities -> read_from_elastic_search-> connect_elastic")
        return
    query  = config.get_this_record
    query["query"]["bool"]["filter"][1]["match_phrase"]["id"] = id
    first_qu = es.search(index="wazuh-alerts-*",body=query)
    dataframe = pd.json_normalize(first_qu["hits"]["hits"])
    return dataframe
    

def write_to_elasticsearch(dataframe,es,index_name):
    if(not es.indices.exists(index_name)):
        es.indices.create(index=index_name,body=config.catboost_ai_settings)
    helpers.bulk(es,generator(dataframe,index_name))
    
    
def get_last_index_knowledge_base():
    es= connect_elasticsearch()
    if (es == False):
        print("Can't connect to Elasticsearch trace: elastic_utilities -> read_from_elastic_search-> get_last_index_knowledge_base")
    if(not es.indices.exists("wazuh-ai-knowledge_base")):
        es.indices.create(index="wazuh-ai-knowledge_base",body=config.catboost_ai_settings)
        return 0
    query  = config.max_index_query
    first_qu=helpers.scan(es,query=query,index="wazuh-ai-knowledge_base")
    res = []
    for item in first_qu:
        res.append(item["_source"])
    dataframe = pd.DataFrame(res)
    if (dataframe.empty):
        return 0
    return dataframe.shape[0]