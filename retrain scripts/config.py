#!/usr/bin/python3

import logging


LOGLEVEL=logging.INFO


########################################## Producer #################################
Wazuh_broadcasting_port = 1111



########################################## Consumer #################################

kafka_topic = "wazuh_alerts"
kafka_bootstrap_server = "10.10.50.12:9092"
consumer_client_id = "ai_node_1"

path_model_1="../models/catboost_model_withContext_1.bin"
path_model_2="../models/catboost_model_withContext_2.bin"


########################################### Elasticsearch ###########################################
elasticsearch_user= "wazuh"
elasticsearch_password = "wazuh"
elasticsearch_ip="10.10.50.2"
elasticsearch_port = "9200"
index_name = "wazuh-ai-correlation"
query = {
  "version": True,
    "size":30,
  "sort": [
    {
      "timestamp": {
        "order": "desc",
        "unmapped_type": "boolean"
      }
    }
  ],
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "30m",
        "time_zone": "Asia/Riyadh",
        "min_doc_count": 1
      }
    }
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    {
      "field": "data.aws.createdAt",
      "format": "date_time"
    },
    {
      "field": "data.aws.end",
      "format": "date_time"
    },
    {
      "field": "data.aws.resource.instanceDetails.launchTime",
      "format": "date_time"
    },
    {
      "field": "data.aws.service.eventFirstSeen",
      "format": "date_time"
    },
    {
      "field": "data.aws.service.eventLastSeen",
      "format": "date_time"
    },
    {
      "field": "data.aws.start",
      "format": "date_time"
    },
    {
      "field": "data.aws.updatedAt",
      "format": "date_time"
    },
    {
      "field": "data.timestamp",
      "format": "date_time"
    },
    {
      "field": "data.vulnerability.published",
      "format": "date_time"
    },
    {
      "field": "data.vulnerability.updated",
      "format": "date_time"
    },
    {
      "field": "syscheck.mtime_after",
      "format": "date_time"
    },
    {
      "field": "syscheck.mtime_before",
      "format": "date_time"
    },
    {
      "field": "timestamp",
      "format": "date_time"
    }
  ],
  "_source": {
    "excludes": [
      "@timestamp"
    ]
  },
  "query": {
    "bool": {
      "must": [],
      "filter": [
        {
          "match_all": {}
        },
        {
          "match_phrase": {
            "data.srcip": "::ffff:192.168.56.1"
          }
        },
        {
          "range": {
            "timestamp": {
              "lte": "2022-08-07T13:16:17.310Z",
              "format": "strict_date_optional_time"
            }
          }
        }
      ],
      "should": [],
      "must_not": []
    }
  },
  "highlight": {
    "pre_tags": [
      "@kibana-highlighted-field@"
    ],
    "post_tags": [
      "@/kibana-highlighted-field@"
    ],
    "fields": {
      "*": {}
    },
    "fragment_size": 2147483647
  }
}

get_this_record = {
  "version": True,
    "size":1,
  "sort": [
    {
      "timestamp": {
        "order": "desc",
        "unmapped_type": "boolean"
      }
    }
  ],
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "30m",
        "time_zone": "Asia/Riyadh",
        "min_doc_count": 1
      }
    }
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    {
      "field": "data.aws.createdAt",
      "format": "date_time"
    },
    {
      "field": "data.aws.end",
      "format": "date_time"
    },
    {
      "field": "data.aws.resource.instanceDetails.launchTime",
      "format": "date_time"
    },
    {
      "field": "data.aws.service.eventFirstSeen",
      "format": "date_time"
    },
    {
      "field": "data.aws.service.eventLastSeen",
      "format": "date_time"
    },
    {
      "field": "data.aws.start",
      "format": "date_time"
    },
    {
      "field": "data.aws.updatedAt",
      "format": "date_time"
    },
    {
      "field": "data.timestamp",
      "format": "date_time"
    },
    {
      "field": "data.vulnerability.published",
      "format": "date_time"
    },
    {
      "field": "data.vulnerability.updated",
      "format": "date_time"
    },
    {
      "field": "syscheck.mtime_after",
      "format": "date_time"
    },
    {
      "field": "syscheck.mtime_before",
      "format": "date_time"
    },
    {
      "field": "timestamp",
      "format": "date_time"
    }
  ],
  "_source": {
    "excludes": [
      "@timestamp"
    ]
  },
  "query": {
    "bool": {
      "must": [],
      "filter": [
        {
          "match_all": {}
        },
        {
          "match_phrase": {
            "id": "::ffff:192.168.56.1"
          }
        },
      ],
      "should": [],
      "must_not": []
    }
  },
  "highlight": {
    "pre_tags": [
      "@kibana-highlighted-field@"
    ],
    "post_tags": [
      "@/kibana-highlighted-field@"
    ],
    "fields": {
      "*": {}
    },
    "fragment_size": 2147483647
  }
}



max_index_query = {
  "version": True,
    "size":1,
  "sort": [
    {
      "_id": {
        "order": "desc",
        "unmapped_type": "boolean"
      }
    }
  ],
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "30m",
        "time_zone": "Asia/Riyadh",
        "min_doc_count": 1
      }
    }
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    {
      "field": "data.aws.createdAt",
      "format": "date_time"
    },
    {
      "field": "data.aws.end",
      "format": "date_time"
    },
    {
      "field": "data.aws.resource.instanceDetails.launchTime",
      "format": "date_time"
    },
    {
      "field": "data.aws.service.eventFirstSeen",
      "format": "date_time"
    },
    {
      "field": "data.aws.service.eventLastSeen",
      "format": "date_time"
    },
    {
      "field": "data.aws.start",
      "format": "date_time"
    },
    {
      "field": "data.aws.updatedAt",
      "format": "date_time"
    },
    {
      "field": "data.timestamp",
      "format": "date_time"
    },
    {
      "field": "data.vulnerability.published",
      "format": "date_time"
    },
    {
      "field": "data.vulnerability.updated",
      "format": "date_time"
    },
    {
      "field": "syscheck.mtime_after",
      "format": "date_time"
    },
    {
      "field": "syscheck.mtime_before",
      "format": "date_time"
    },
    {
      "field": "timestamp",
      "format": "date_time"
    }
  ],
  "_source": {
    "excludes": [
      "@timestamp"
    ]
  },
  "query": {
    "bool": {
      "must": [],
      "filter": [
        {
          "match_all": {}
        }
      ],
      "should": [],
      "must_not": []
    }
  },
  "highlight": {
    "pre_tags": [
      "@kibana-highlighted-field@"
    ],
    "post_tags": [
      "@/kibana-highlighted-field@"
    ],
    "fields": {
      "*": {}
    },
    "fragment_size": 2147483647
  }
}

# catboost_ai_settings={
#     "settings":{
#         "number_of_shards":1,
#         "number_of_replicas":0,     
#     },
#     "mappings":{
#         "properties":{
#             "rule.frequency":{
#                 "type":"text"
#             },
#             "timestamp":{
#                 'type':"date",
#                 "format": "date_optional_time"
#             }
#         }
#     }
# }



catboost_ai_settings={
        "settings":{
            "number_of_shards":1,
            "number_of_replicas":0,     
        },
            "mappings" : {
      "properties" : {
        "agent_description" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "agent_id" : {
              "type" : "keyword"
        },
        "agent_ip" : {
          "type" : "keyword"
        },
        "agent_name" : {
              "type" : "keyword"
        },
        "data_id" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
            }
          }
        },
        "data_protocol" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"           
             }
          }
        },
        "data_srcip" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "data_url" : {
          "type" : "text"
        },
        "decoder_name" : {
          "type" : "text"
        },
        "full_log" : {
          "type" : "text"
    
        },
        "history_T1055" : {
          "type" : "long"
        },
        "history_T1064" : {
          "type" : "long"
        },
        "history_T1068" : {
          "type" : "long"
        },
        "history_T1083" : {
          "type" : "long"
        },
        "history_T1190" : {
          "type" : "long"
        },
        "history_T1210" : {
          "type" : "long"
        },
        "history_T1212" : {
          "type" : "long"
        },
        "history_count_events" : {
          "type" : "long"
        },
        "history_rule_firedtimes" : {
          "type" : "long"
        },
        "history_source_data_id_200" : {
          "type" : "long"
        },
        "history_source_data_id_300" : {
          "type" : "long"
        },
        "history_source_data_id_400" : {
          "type" : "long"
        },
        "history_source_data_id_500" : {
          "type" : "long"
        },
        "id" : {
          "type" : "text"
        },
        "input_type" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
            }
          }
        },
        "location" : {
          "type" : "keyword"
        },
        "manager_name" : {
          "type" : "keyword"
        },
        "output_1" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
            }
          }
        },
        "output_2" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "rule_frequency" : {
              "type" : "keyword"
        },
        "rule_description" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
            }
          }
        },
        "rule_firedtimes" : {
          "type" : "long"
        },
        "rule_frequency" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "rule_gdpr" : {
              "type" : "keyword"
        },
        "rule_groups" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "rule_hipaa" : {

              "type" : "keyword"    
        },
        "rule_id" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "rule_level" : {
          "type" : "long"
        },
        "rule_mail" : {
          "type" : "boolean"
        },
        "rule_mitre_id" : {
          "type" : "keyword"

        },
        "rule_nist_800_53" : {

              "type" : "keyword",

        },
        "rule_pci_dss" : {

              "type" : "keyword",

        },
        "rule_tsc" : {
              "type" : "keyword"
        },
        "timestamp" : {
          "type" : "date",
          "format" : "date_optional_time"
        }
      }
    }
  
      }
