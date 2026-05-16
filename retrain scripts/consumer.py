#!/usr/bin/python3

try:
    import json
    from kafka import KafkaConsumer
    import pandas as pd
    from attack_classifier import run_catboost_ai_multicalssifier_model
    from elastic_utilities import connect_elasticsearch
    from elastic_utilities import read_from_elastic_search
    from elastic_utilities import write_to_elasticsearch
    from config import kafka_topic
    from config import kafka_bootstrap_server
    from config import consumer_client_id
    import warnings
    import time
    from datetime import datetime
    from datetime import date
    from ai_adaptive_retrain import check_worth_new_model
    from ai_adaptive_retrain import scan_knowledgebase
    from ai_adaptive_retrain import train_new_models
    from catboost import CatBoostClassifier
    from config import path_model_1
    from config import path_model_2
    from config import index_name
    

except Exception as e :
    print("Some Modules are Missing in Consumer.py {}".format(e))

warnings.filterwarnings("ignore")

def eval_json(data):
    # print(data)
    temp = json.loads(data)
    temp = temp[temp.find('{'):]
    tt = temp[:temp.find('"full_log"')-1]
    vv = temp[temp.find('"decoder"') -1:]
    new_temp = tt + vv    
    temp_dict = json.loads(new_temp)
    dataframe = pd.json_normalize(temp_dict)
    return dataframe




def change_models():
    es = connect_elasticsearch()

    dataframe = scan_knowledgebase(es)
    if(not check_worth_new_model(dataframe)):
        print("Training New Models !")
        train_new_models(dataframe)
    else:
        print("No Need for new Models..")



def run_kafka_consumer(consumer):
        starting_date = datetime.now()
        # change_models()
        model_1 = CatBoostClassifier()
            
        model_2 = CatBoostClassifier()
        
        model_1.load_model(path_model_1)
        model_2.load_model(path_model_2)
        num_drop=0    
        for msg in consumer:
            now_date = datetime.now()
            dif = now_date - starting_date
            if(dif.days>=1):
                print("diff is more than one day!!!!!!!!")
                # change_models()
                model_1.load_model(path_model_1)
                model_2.load_model(path_model_2)
                
  
            data = json.loads(msg.value)
            datastr = str(data)
            if(("AH01114" in datastr)):
                print("continue")
                continue
            
            dataframe = eval_json(msg.value)
            columns = list(dataframe.columns)
            if(("data.srcip" not in columns) or ("id" not in columns) or ("timestamp" not in columns)):
                num_drop+=1
                print("dropped " , num_drop)
                continue
            src_id = dataframe["id"][0]
            timestamp = dataframe["timestamp"][0]
            src_ip =  dataframe["data.srcip"][0]
            es = connect_elasticsearch()
            # logging.debug(src_id)
            ## read the history from Elasticsearch
            dataframe = ""
            while True:
                dataframe = read_from_elastic_search(src_ip,timestamp,es)
                if("_source.id" not in list(dataframe.columns)):
                    continue
                if(src_id in list(dataframe["_source.id"])):
                    break
                print("wait")
                time.sleep(2)
            
            # ## classify this record with the use of its context
            dataframe = run_catboost_ai_multicalssifier_model(dataframe,src_id,model_1,model_2)
            # print("the shape before writing " ,dataframe.shape)
            
            ## write the result to elasticsearch index pattern wazuh-ai-catboost
            
            # today = date.today()
            # index_name ="wazuh-ai-catboost-"+str(today.year)+'.'+str(today.month)+'.'+str(today.day)
            write_to_elasticsearch(dataframe,es,index_name)
      
      

if __name__ == "__main__":

    consumer = KafkaConsumer(kafka_topic,
                          bootstrap_servers=kafka_bootstrap_server,
                          auto_offset_reset="earliest",
                          client_id = consumer_client_id,
                        group_id=consumer_client_id)
    
   
    if (consumer.bootstrap_connected()):
        print("Kafka Consumer Started !")
        run_kafka_consumer(consumer)
    else:
        print("Consumer Can't Connect to Kafka Server !!")

