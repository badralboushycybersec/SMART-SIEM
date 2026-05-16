#!/usr/bin/python3


try :
    from config import path_model_1
    from config import path_model_2
    from features import category_features
    from features import all_features
    from features import numerical_features
    from features import mirtre_id_attacks
    import time
    from catboost import CatBoostClassifier
    from elastic_utilities import read_elasticrecord
    from elastic_utilities import connect_elasticsearch

    import pandas as pd
    import numpy as np
    import logging

except Exception as e :
    print("Some Modules are Missing in attack_classifier.py {}".format(e))


def preprocessing(df):  
    
    #these category features if they didn't exist we will add them to the dataframe
    
    list_test_columns= list(df.columns)
    for i in range ( 0, len(category_features)):
        if(category_features[i] not in list_test_columns):
            df[category_features[i]] = " "
    for c in numerical_features:
        if(c not in list_test_columns):
            df[c] = 1
            
            
    # fill the numerical values of histry attributes with zeroes
    
    df["history._source.rule.firedtimes"] = 1
    df["history._source.data.id.200"]= 0
    df["history._source.data.id.300"]= 0
    df["history._source.data.id.400"]= 0
    df["history._source.data.id.500"]= 0
    for item in mirtre_id_attacks:
        df[item] = 0
    # fill the columns that has None values with empty strings.
    
    for c in category_features:
        if(df[c].isnull().any()):
            df[c] = df[c].fillna(' ')
    
    # fill the columns rule level with rule.level = 3
    
    df["_source.rule.level"] = df["_source.rule.level"].fillna(3)
    df["_source.rule.firedtimes"] = df["_source.rule.firedtimes"].fillna(1)
    
    
    # fill mail values with 1 and 0 
    
    for index,row in df.iterrows(): 
        df.at[index,'_source.rule.frequency'] = str(row['_source.rule.frequency'])
        
        if(isinstance(row["_source.rule.id"],int)):
            df.at[index,'_source.rule.id'] = str(row['_source.rule.id'])
        
        for cat_fe in category_features:
            if(isinstance(row[cat_fe],list)):
                df.at[index,cat_fe] = str(row[cat_fe])
        if (row["_source.rule.mail"]==True):
            df.at[index,"_source.rule.mail"] = 1
        else :
            df.at[index,"_source.rule.mail"] = 0
            
        if(row["_source.data.id"] == ' '):
            df.at[index,"_source.data.id"] = 200
        else :
            # print(row["_source.data.id"])
            # print(row)
            try:
                df.at[index,"_source.data.id"] = int(row["_source.data.id"])
                    
            except Exception as e :
                df.at[index,"_source.data.id"] = 200
    
    df = df.fillna(' ')

    return df




def add_history(dataframe,id):
    dataframe["count_events"] = 1
    max_firedtimes = 1
    num = 0 
    # # print("id is ",id)
    # # print("comming index ",dataframe.iloc[0]["_source.id"])
    # if (dataframe.iloc[0]["_source.id"] != id):
    #     es = connect_elasticsearch()
    #     dataframe_1 = read_elasticrecord(id, es)
    #     print("shape of dataframe",dataframe_1.shape)
    #     if( dataframe_1.empty):
    #         time.sleep(2)
    #         return add_history(dataframe, id)
    #     dataframe_1=preprocessing(dataframe_1)
    #     # print("dataframe 1 ",dataframe["_source.rule.firedtimes"][0])
    #     dataframe = pd.concat([dataframe_1,dataframe],axis=0)
    #     dataframe = dataframe.reset_index(drop=True)
        
    for index,row in dataframe.iterrows():
        num+=1
        max_firedtimes = max(max_firedtimes,dataframe.at[index,"_source.rule.firedtimes"])
        
        temp = dataframe.at[index,'_source.data.id']//10
        if (temp == 20):
           dataframe.at[0,'history._source.data.id.200'] += 1
        elif (temp == 30):
           dataframe.at[0,'history._source.data.id.300'] += 1
        elif (temp == 40):
           dataframe.at[0,'history._source.data.id.400'] += 1
        elif (temp == 50):
           dataframe.at[0,'history._source.data.id.500'] += 1
        
        
        temp = dataframe.at[index,"_source.rule.mitre.id"]
        for item in mirtre_id_attacks:
            if(item in temp):
                dataframe.at[0,item] = dataframe.at[0,item] + 1
    # logging.debug("max fired times{} ".format(max_firedtimes))
    dataframe.at[0,"history._source.rule.firedtimes"] = max_firedtimes
    dataframe.at[0,"count_events"] = num
    dataframe['_source.agent.description'] = "APACHE_SERVER"
    return dataframe.iloc[[0],:]



def label_data(dataframe,model_1,model_2):
    # model_1 = CatBoostClassifier()
        
    # model_2 = CatBoostClassifier()
    
    # model_1.load_model(path_model_1)
    # model_2.load_model(path_model_2)

    df = dataframe[all_features]
    
    res =[ str(x) for x in df.iloc[0].values]
#    file = open("logs.txt","a")
#    file.writelines(str(df.iloc[0]))
    
    
    prediction_1 = model_1.predict(df)
    prediction_2 = [["NORMAL"]]
    if(prediction_1 != "NORMAL"):
        prediction_2 = model_2.predict(df)
    dataframe["output_1"] = prediction_1
    dataframe["output_2"] = prediction_2[0][0]
    if(prediction_1[0]=="NORMAL"):
        print(str(prediction_1[0]))
    else :
        print(str(prediction_2[0][0]))

#    file.write ("     preditions : ")
#    file.write(str(prediction_1) + "  " + str(prediction_2))
#    file.write("\n#####################################\n")

#    file.close()

    return dataframe


def run_catboost_ai_multicalssifier_model(dataframe,src_id,model_1,model_2):

    
    # get the predictions
    
    if(not dataframe.empty):
        dataframe = preprocessing(dataframe)
        dataframe = add_history(dataframe,src_id)
        dataframe= label_data(dataframe,model_1,model_2)
        return dataframe




   
    
   
