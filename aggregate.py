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
            "session_id": {
                "terms": {
                    "field": "session_id.keyword",
                    "size": 10000000
                }
            }
        }
    }
    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    results = json.loads(response.text)
    if "error" in results:
        print(json.dumps(results, indent=4))
        return []
    else:
        return [bucket["key"] for bucket in results["aggregations"]["session_id"]["buckets"]]


def get_session(uri, session_id):
    """(object) Get all the user actions, client log messages of a session. All the data is aggregated
    as the predefined query.

    Parameters:
        uri (string): The uri of ES search API including the index name
        session_id (string): the Session ID to search

    """
    query = {
        "size": 0,
        "query": {
            "match": {
                "session_id": session_id
            }
        },
        "aggs": {
            "ip_address": {
                "terms": {
                    "field": "content.details.ip.keyword"
                }
            },
            "fingerprint": {
                "terms": {
                    "field": "content.details.fingerprint"
                }
            },
            "message_count": {
                "terms": {
                    "field": "log_type.keyword"
                }
            },
            "assignment_id": {
                "terms": {
                    "field": "assignment_id.keyword"
                }
            },
            "worker_id": {
                "terms": {
                    "field": "worker_id.keyword"
                }
            },
            "hit_id": {
                "terms": {
                    "field": "hit_id.keyword"
                }
            },
            "start_time": {
                "min": {
                    "field": "browser_time"
                }
            },
            "end_time": {
                "max": {
                    "field": "browser_time"
                }
            }
        }
    }

    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    data = json.loads(response.text)

    result = {
        "session_id": session_id,
        "message_count": data["aggregations"]["message_count"]["buckets"],
        "total_count": data["hits"]["total"],
        "start_time": data["aggregations"]["start_time"]["value_as_string"],
        "end_time": data["aggregations"]["end_time"]["value_as_string"],
        "duration": data["aggregations"]["end_time"]["value"] - data["aggregations"]["start_time"]["value"]
    }

    for aggs in ("worker_id", "hit_id", "assignment_id", "ip_address", "fingerprint"):
        if len(data["aggregations"][aggs]["buckets"]) > 0:
            data[aggs] = data["aggregations"][aggs]["buckets"][0]["key"]

    return result


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


def main(date):
    """(bool) Aggregate multiple messages of a session into a single record and index it to ES

    Parameters:
        date (string): the log date need to be aggregate (%y-%m-%d)
    """

    print("Delete Old Index:", date, delete_index(base_uri + "/" + session_index_prefix + "-" + date))

    sessions = get_sessions(base_uri + "/" + log_index_prefix + "-" + date + "/_search")
    for session_id in sessions:
        session = get_session(base_uri + "/" + log_index_prefix + "-" + date + "/_search", session_id)
        if session is not None:
            doc_id = add_session(base_uri + "/" + session_index_prefix + "-" + date + "/session", session)
            print(date, session_id, doc_id)


if __name__ == '__main__':
    main(sys.argv[1])



