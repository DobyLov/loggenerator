# es_settings

index_template = {
  "index_patterns": ["loggen-*"], 
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.lifecycle.name": "ilm_loggen", 
    "index.lifecycle.rollover_alias": "loggen-alias"
  }
}

test_index_template = {
  "index_patterns": ["loggen-*"], 
  "settings": {
    "index.lifecycle.name": "ilm_loggen", 
    "index.lifecycle.rollover_alias": "loggen-alias"
  }
}

# es_index_settings
settings = {
  "settings" : {
      "index" : {
        "number_of_shards" : "1",
        "number_of_replicas" : "0",
        "write" : {
          "wait_for_active_shards" : "1"
        }
      }
  }
}


# es_mapping
mapping = {
	"properties": {
		"age": {
			"type": "long"
		},
		"country": {
			"properties": {
				"country_long": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"country_short": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"location": {
					"properties": {
						"latitude": {
							"type": "text",
							"fields": {
								"keyword": {
									"type": "keyword",
									"ignore_above": 256
								}
							}
						},
						"longitude": {
							"type": "text",
							"fields": {
								"keyword": {
									"type": "keyword",
									"ignore_above": 256
								}
							}
						}
					}
				},
				"region": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"time_zone": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"town": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"dateTime": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"hasTags": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"ip_address": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"message_tweet": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"user": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"uuid": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		}
	}

}


