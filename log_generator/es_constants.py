""" es_constants """

# ES pipeline, index, templates, ilm

# Pipeline
user_agent_pipeline_name = "pipeline_user_agent"
pipeline_user_agent = {
    "description" : "Parse and add user agent information",
    "version": 100,
    "processors" : [
        {
            "geoip" : {
                "field" : "ip_address"
            }
        },
        {
            "user_agent" : {
                "field" : "userAgent"
            }
        }
    ]
}

# Index
index_name_pyloggen = "pyloggen_"
index_logRotateStrategy = {}
index_ilmStrategy = {}
index_mapping = {
     "properties" : {
        "age" : {
            "type" : "long"
        },
        "country" : {
            "properties" : {
            "country_long" : {
                "type" : "text",
                "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
                }
            },
            "country_short" : {
                "type" : "text",
                "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
                }
            },
            "location" : {
                "properties" : {
                "latitude" : {
                    "type" : "text",
                    "fields" : {
                    "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                    }
                    }
                },
                "longitude" : {
                    "type" : "text",
                    "fields" : {
                    "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                    }
                    }
                }
                }
            },
            "region" : {
                "type" : "text",
                "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
                }
            },
            "time_zone" : {
                "type" : "text",
                "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
                }
            },
            "town" : {
                "type" : "text",
                "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
                }
            }
            }
        },
        "dateTime" : {
            "type" : "date",
            "format": "yyyy-MM-dd'T'HH:mm:ss"
        },
        "hasTags" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "ip_address" : {
            "type" : "ip"
        },
        "message_tweet" : {
            "type" : "text",
            "fields" : {
            "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
            }
            }
        },
        "user" : {
            "type" : "text",
            "fields" : {
            "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
            }
            }
        },
        "uuid" : {
            "type" : "text",
            "fields" : {
            "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
            }
            }
        },
        "userAgent" : {
            "type" : "text"
        }
    }
}

# Templates
index_template_name = ".pyloggen_template"
index_template_settings_1 = {
  "index_patterns": ["pyloggen_*"], 
  "settings": {
    "index.default_pipeline": "pipeline_user_agent",
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.lifecycle.rollover_alias": "pyloggen_alias"
  },
  "mappings": index_mapping 
}

index_template_settings_2 = {
  "index_patterns": ["pyloggen_*"], 
  "settings": {
    "index.default_pipeline": "pipeline_user_agent",
    "number_of_shards": 1,
    "number_of_replicas": 1,
    "index.lifecycle.rollover_alias": "pyloggen_alias"
  },
  "mappings": index_mapping 
}

index_template_settings_3 = {
  "index_patterns": ["pyloggen_*"], 
  "settings": {
    "index.default_pipeline": "pipeline_user_agent",
    "number_of_shards": 2,
    "number_of_replicas": 2,
    "index.lifecycle.rollover_alias": "pyloggen_alias"
  },
  "mappings": index_mapping 
}

index_template_settings_4 = {
  "index_patterns": ["pyloggen_*"], 
  "settings": {
    "index.default_pipeline": "pipeline_user_agent",
    "number_of_shards": 3,
    "number_of_replicas": 2,
    "index.lifecycle.rollover_alias": "pyloggen_alias"
  },
  "mappings": index_mapping 
}
#   "index.lifecycle.name": "loggen_ilm_policy", 
# "format": "EEE MMM dd HH:mm:ss Z yyyy"