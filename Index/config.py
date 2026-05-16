




########################################### Elasticsearch ###########################################
elasticsearch_user= "wazuh"
elasticsearch_password = "wazuh"
elasticsearch_ip="192.168.56.104"
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

catboost_ai_settings={
    "settings":{
        "number_of_shards":1,
        "number_of_replicas":0,     
    },
    "mappings":{
        "properties":{
            "rule.frequency":{
                "type":"text"
            },
            "timestamp":{
                'type':"date",
                "format": "date_optional_time"
            }
        }
    }
}