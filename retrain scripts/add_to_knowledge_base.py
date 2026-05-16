#!/usr/bin/python3

try :
    import pandas as pd
    from elastic_utilities import connect_elasticsearch
    from elastic_utilities import get_last_index_knowledge_base
    from elastic_utilities import write_to_elasticsearch
    from features import category_features
    from features import all_features
    from features import numerical_features
    import warnings
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
    



def write_to_knowledge_base(path,es):
    dataframe = pd.read_csv(path)
    last_index = int(get_last_index_knowledge_base())
    dataframe = dataframe.reindex(labels = [x for x in range (last_index,dataframe.shape[0] + last_index)])
    dataframe = preprocessing(dataframe)
    print("last index",last_index)
    print("training dataset shape : ",dataframe.shape)
    write_to_elasticsearch(dataframe, es, "wazuh-ai-knowledge_base")
    print("Finished!!")
    



if  __name__ == "__main__":
    es = connect_elasticsearch()
    if (es == False ):
        print("Can't connect to Elasticsearch trace: add_to_knowledge_base -> __main__-> connect_elastic")
    else:
        path= input("please Enter the path of the Dataset you want to add it To Wazuh ai kowledgebase!\n")
        write_to_knowledge_base(path, es)
   
   
