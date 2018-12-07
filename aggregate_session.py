import requests
import json
import sys

log_index_prefix = "uqcrowd-log"
session_index_prefix = "uqcrowd-session"
base_uri = "http://localhost:9200"


def get_sessions(uri):
    """Get all unique Session ID from the log index.

    Parameters:
        uri (string): The uri of ES search API including the index name
    """
    query = {
        "size": 0,
        "aggs": {
            "session": {
                "terms": {
                    "field": "session",
                    "size": 1000000
                }
            }
        }
    }
    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    results = json.loads(response.text)
    if "error" in results:
        print(json.dumps(results, indent=4))
        return None
    else:
        return [bucket["key"] for bucket in results["aggregations"]["session"]["buckets"]]


def get_session(uri, session_id):
    """(object) Get all the user actions, client log messages of a session. All the data is aggregated
    as the predefined query.

    Parameters:
        uri (string): The uri of ES search API including the index name
        session_id (string): the Session ID to search

    """
    query = {
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
    }

    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
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


def add_session(uri, session):
    """(string) Insert a session into the ES index,
    return the doc_id of the record if successful, return None otherwise

    Parameters:
        uri (string): The uri of ES indexing API including the index name and doc type
        session (object): the session need to be indexed

    """
    response = requests.post(uri, headers={"Content-Type": "application/json"}, data=json.dumps(session))
    results = json.loads(response.text)
    return results["_id"] if results.get("result") == "created" else None


def delete_index(uri):
    """(bool) Delete an index on ES, use to clean up previous results

    Parameters:
        uri (string): The uri of ES deleting index API including the index name
    """
    response = requests.delete(uri, headers={"Content-Type": "application/json"})
    results = json.loads(response.text)
    return results.get("acknowledged")


def update_mapping(uri):
    """(bool) Update the mapping of an uqcrowd-log index, set the fielddata parameter of "Session" field to True
    Todo: this is sort of a hardcoded workaround method to address the invalid data type issue

    Parameters:
        uri (string): The uri of ES deleting index API including the index name
    """
    query = {
        "properties": {
            "session": {
                "type": "text",
                "fielddata": True
            }
        }
    }
    response = requests.put(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    results = json.loads(response.text)
    return results.get("acknowledged")


def main(date):
    """(bool) Aggregate multiple messages of a session into a single record and index it to ES

    Parameters:
        date (string): the log date need to be aggregate (%y-%m-%d)
    """
    print("Update Mapping:", update_mapping(base_uri + "/" + log_index_prefix + "-" + date + "/_mapping/" + log_index_prefix))
    print("Delete Old Index:", date, delete_index(base_uri + "/" + session_index_prefix + "-" + date))

    sessions = get_sessions(base_uri + "/" + log_index_prefix + "-" + date + "/_search")
    for session_id in sessions:
        session = get_session(base_uri + "/" + log_index_prefix + "-" + date + "/_search", session_id)
        if session is not None:
            doc_id = add_session(base_uri + "/" + session_index_prefix + "-" + date + "/session", session)
            print(session_id, doc_id)


if __name__ == '__main__':
    main(sys.argv[1])



