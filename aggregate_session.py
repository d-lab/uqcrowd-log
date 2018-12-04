import requests
import json
import sys

log_index_prefix = "uqcrowd-log"
session_index_prefix = "uqcrowd-session"
base_uri = "http://localhost:9200"


def get_sessions(uri):
    query = json.dumps({
        "size": 0,
        "aggs": {
            "session": {
                "terms": {
                    "field": "session",
                    "size": 1000000
                }
            }
        }
    })
    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=query)
    results = json.loads(response.text)
    if "error" in results:
        print(json.dumps(results, indent=4))
        return None
    else:
        return [bucket["key"] for bucket in results["aggregations"]["session"]["buckets"]]


def get_session(uri, session_id):
    query = json.dumps({
        "query": {
            "match": {
                "session": session_id
            }
        },
        "size": 0,
        "aggs": {
            "start_time": {
                "min": {
                    "field": "timestamp"
                }
            },
            "end_time": {
                "max": {
                    "field": "timestamp"
                }
            },
            "task_id": {
                "max": {
                    "field": "task_id"
                }
            },
            "worker_id": {
                "max": {
                    "field": "worker_id"
                }
            },
            "final_checks_passed": {
                "filter": {
                    "term": {
                        "message.final_checks_passed": "true"
                    }
                }
            }
        }
    })

    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=query)
    results = json.loads(response.text)

    if results["hits"]["total"] > 0:
        return {
            "session_id": session_id,
            "message_count": results["hits"]["total"],
            "worker_id": results["aggregations"]["worker_id"]["value"],
            "task_id": results["aggregations"]["task_id"]["value"],
            "start_time": results["aggregations"]["start_time"]["value_as_string"],
            "end_time": results["aggregations"]["end_time"]["value_as_string"],
            "duration": results["aggregations"]["end_time"]["value"] - results["aggregations"]["start_time"]["value"],
            "final_checks_passed": results["aggregations"]["final_checks_passed"]["doc_count"] > 0
        }
    else:
        return None


def post_session(uri, session):
    response = requests.post(uri, headers={"Content-Type": "application/json"}, data=json.dumps(session))
    results = json.loads(response.text)
    return results["_id"] if results["result"] == "created" else None


def fix_index_mapping(uri):
    query = json.dumps({
        "properties": {
            "session": {
                "type": "text",
                "fielddata": True
            }
        }
    })
    response = requests.put(uri, headers={"Content-Type": "application/json"}, data=query)
    results = json.loads(response.text)
    print(json.dumps(results))


def main(date):

    fix_index_mapping(base_uri + "/" + log_index_prefix + "-" + date + "/_mapping/" + log_index_prefix)

    sessions = get_sessions(base_uri + "/" + log_index_prefix + "-" + date + "/_search")
    for session_id in sessions:
        session = get_session(base_uri + "/" + log_index_prefix + "-" + date + "/_search", session_id)
        if session is not None:
            doc_id = post_session(base_uri + "/" + session_index_prefix + "-" + date + "/session", session)
            print(session_id, doc_id)


if __name__ == '__main__':
    main(sys.argv[1])



