try :
    import pandas as pd

    from features import category_features
    from features import all_features
    from features import numerical_features
    from config import elasticsearch_user
    from config import elasticsearch_password
    from config import elasticsearch_ip
    from config import elasticsearch_port
    from config import catboost_ai_settings
    from elasticsearch import Elasticsearch
    from elasticsearch import helpers
    import warnings

except Exception as e :
    print("Some Modules are Missing{}".format(e))
    
warnings.filterwarnings("ignore")




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


    
def preprocessing(df):  
    #these category features if they didn't exist we will add them to the dataframe
    list_test_columns= list(df.columns)
    for i in range ( 0, len(category_features)):
        if(category_features[i] not in list_test_columns):
            df[category_features[i]] = " "
    for c in numerical_features:
        if(c not in list_test_columns):
            df[c] = 1
    # fill the columns that has None values with empty strings.
    for c in category_features:
        if(df[c].isnull().any()):
            df[c] = df[c].fillna(' ')
    # fill the columns rule level with rule.level = 3
    df["_source.rule.level"] = df["_source.rule.level"].fillna(1)
    df["_source.rule.firedtimes"] = df["_source.rule.firedtimes"].fillna(1)

    # fill mail values with 1 and 0 
    for index,row in df.iterrows():

        if(isinstance(row["_source.rule.id"],int)):
            df.at[index,'_source.rule.id'] = str(row['_source.rule.id'])
        
        for cat_fe in category_features:
            if(isinstance(row[cat_fe],list)):
                df.at[index,cat_fe] = str(row[cat_fe])
        if (row["_source.rule.mail"]==True):
            df.at[index,"_source.rule.mail"] = 1
        else :
            df.at[index,"_source.rule.mail"] = 0
    df = df.fillna(' ')
    return df
    
def connect_elasticsearch():
    user=elasticsearch_user
    password = elasticsearch_password
    ip=elasticsearch_ip
    port = elasticsearch_port
    es = Elasticsearch(["https://" + user + ":"+password+"@"+ip+":"+port], verify_certs=False)
    if(es.ping()):
        return es
    return False


def write_to_elasticsearch(dataframe,es,index_name):
    if(not es.indices.exists(index_name)):
        es.indices.create(index=index_name,body=catboost_ai_settings)
    helpers.bulk(es,generator(dataframe,index_name))
    




def read_data(path,es):
    dataframe = pd.read_csv(path)
    dataframe = preprocessing(dataframe)
  
    write_to_elasticsearch(dataframe, es, "wazuh-ai-correlation")
    print("Finished!!")
    



if  __name__ == "__main__":
    es = connect_elasticsearch()
    if (es == False ):
        print("Can't connect to Elasticsearch trace: add_to_knowledge_base -> __main__-> connect_elastic")
    else:
        path= "./ai_data.csv"
        read_data(path, es)
   
   
