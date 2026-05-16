#!/usr/bin/python3
try :
    from datetime import date
    import datetime
    import time
    from catboost import Pool
    from catboost import CatBoostClassifier
    from elasticsearch import Elasticsearch
    from elasticsearch import helpers
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    import os
    import sys
    import pandas as pd
    import numpy as np
    import numpy as np
    import warnings
    from features import all_features
    from features import category_features
    from features import numerical_features
    from config import path_model_1
    from config import path_model_2
    

except Exception as e :
    print("Some Modules are Missing{}".format(e))
warnings.filterwarnings("ignore")


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




def scan_knowledgebase(es):
    query={"query": {
            "match_all": {}
            }
        }
    firstq=helpers.scan(es,query=query,
        index="wazuh-ai-knowledge_base")
    res = []
    for item in firstq:
        res.append(item["_source"])
    df = pd.DataFrame(res)
    df = rename_df(df)
    df = preprocessing(df)
    return df



def check_worth_new_model(df):
    model_1 = CatBoostClassifier()
        
    model_2 = CatBoostClassifier()
    
    model_1.load_model(path_model_1)
    model_2.load_model(path_model_2)
    predictions_1 = model_1.predict(df[all_features])
    df["output"] = predictions_1
    temp_df = df[df["output"] != "NORMAL"]
    predictions_2 = model_2.predict(temp_df[all_features])
    i = 0
    for index,row in df.iterrows():
        if(row["output"] == "ATTACK"):
            df.at[index,"output"] = predictions_2[i]
            i+=1

    count=0
    for index,row in df.iterrows():
        if(row["output_2"] == row["output"]):
            count+=1

    number_of_rows = df.shape[0]
    ratio =count*100/number_of_rows
    if(ratio > 90):
        print("The Old Model predicts " ,str(ratio)+"%" , "From the Data Successfully!..no need for new models")
        return False
    print("The Old Model predicts " ,str(ratio)+"%")
    return True

def rename_df(df):
    dataframe_renamed= df.rename(columns={

                        'data_protocol':'_source.data.protocol',
                        'data_id'  :'_source.data.id',
                        'rule_firedtimes' :'_source.rule.firedtimes',
                        'rule_mail'  :'_source.rule.mail',
                        'rule_level'     :'_source.rule.level',
                        'rule_description' :'_source.rule.description',
                        'rule_groups' :'_source.rule.groups',
                        'rule_pci_dss'  :'_source.rule.pci_dss',
                        'rule_tsc' :'_source.rule.tsc',
                        'rule_nist_800_53' :'_source.rule.nist_800_53',
                        'rule_gdpr'  :'_source.rule.gdpr',
                        'rule_mitre_id'  :'_source.rule.mitre.id',
                        'rule_frequency' :'_source.rule.frequency',
                        'rule_hipaa'  :'_source.rule.hipaa',
                        'agent_description'  :'_source.agent.description',
                        'rule_id'    :'_source.rule.id',
                        'history_rule_firedtimes'   :'history._source.rule.firedtimes',
                        'history_source_data_id_200' :'history._source.data.id.200',
                        'history_source_data_id_300'   :'history._source.data.id.300',
                        'history_source_data_id_400'  :'history._source.data.id.400',
                        'history_source_data_id_500'  :'history._source.data.id.500',
                        'history_T1212'  :'T1212',
                        'history_T1068' :'T1068',
                        'history_T1064'   :'T1064',
                        'history_T1210' :'T1210',
                        'history_T1083' :'T1083',
                        'history_T1055'  :'T1055',
                        'history_T1190'   :'T1190'
    })
    return dataframe_renamed



def train_new_models(dataframe):
    all_features_1= all_features
    all_features_1.append("output_1")
    all_features_1.append("output_2")
    dataframe = dataframe[all_features_1]
    y1= dataframe["output_1"]
    X1 = dataframe.drop(['output_1','output_2'], axis=1)
    X1_train,X1_validation,y1_train,y1_validation = train_test_split(X1,y1,test_size=0.2,random_state=0)
    train_pool_1 =Pool(
        data=X1_train,
        label=y1_train,
        cat_features = category_features,
    )

    test_pool_1 = Pool(
        data=X1_validation,
        label=y1_validation,
        cat_features=category_features,
    )
    model_1 = CatBoostClassifier(
    iterations=1000)
    
    model_1.fit(
        train_pool_1,
        eval_set=test_pool_1,
        verbose=100,
        plot=False
    )
    
    dataframe_2 = dataframe[dataframe["output_2"] != "NORMAL" ]
    y2= dataframe_2["output_2"]
    X2 = dataframe_2.drop(['output_1','output_2'], axis=1)


    X2_train,X2_validation,y2_train,y2_validation = train_test_split(X2,y2,test_size=0.2,random_state=0)
    train_pool_2 =Pool(
        data=X2_train,
        label=y2_train,
        cat_features = category_features,
    )

    test_pool_2 = Pool(
        data=X2_validation,
        label=y2_validation,
        cat_features=category_features,
    )
    
    model_2 = CatBoostClassifier(
    iterations=1000)
    
    model_2.fit(
        train_pool_2,
        eval_set=test_pool_2,
        verbose=100,
        plot=False
    )
    
    y1_predict = model_1.predict(X1_validation)
    
    y2_predict = model_2.predict(X2_validation)

    print("the First Stage")
    print(classification_report(y1_validation, y1_predict))
    print("*"*100)
    print("the Second Stage")
    print(classification_report(y2_validation,y2_predict))
    # model_1.save_model(path_model_1)
    # model_2.save_model(path_model_2)
    print("Training New AI Models Finished !")
    