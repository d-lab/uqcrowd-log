from flask import Flask, request, Response, send_file
import json
import requests
import sys

app = Flask(__name__)
api_prefix = "/analytics"
base_uri = "http://localhost:9200/uqcrowd-session-*/_search"


# Aggregate by worker id
@app.route(api_prefix + "/session/worker/<worker_id>", methods=['GET'])
def worker(worker_id):
    data = search({
        "query": {
            "match": {
                "worker_id": worker_id
            }
        }
    })
    results = [session['_source'] for session in data['hits']['hits']]
    return Response(json.dumps(results), mimetype="application/json")


@app.route(api_prefix + "/session/worker/<worker_id>/histogram", methods=['GET'])
def worker_histogram(worker_id):
    return histogram("worker_id", worker_id)


@app.route(api_prefix + "/session/worker/<worker_id>/aggregation", methods=['GET'])
def worker_aggregation(worker_id):
    return aggregation("worker_id", worker_id)


# Aggregate by client fingerprint
@app.route(api_prefix + "/session/client/<fingerprint>", methods=['GET'])
def client(fingerprint):
    data = search({
        "query": {
            "match": {
                "worker_id": fingerprint
            }
        }
    })
    sessions = [session['_source'] for session in data['hits']['hits']]
    return Response(json.dumps(sessions), mimetype="application/json")


@app.route(api_prefix + "/session/worker/<fingerprint>/histogram", methods=['GET'])
def client_histogram(fingerprint):
    return histogram("fingerprint", fingerprint)


@app.route(api_prefix + "/session/worker/<fingerprint>/aggregation", methods=['GET'])
def client_aggregation(fingerprint):
    return aggregation("fingerprint", fingerprint)


# Supporting Methods
def search(query):
    response = requests.get(base_uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    return json.loads(response.text)


def histogram(criteria, value):
    data = search({
        "size": 0,
        "query": {
            "match": {
                criteria: value
            }
        },
        "aggs": {
            "session": {
                "date_histogram": {
                    "field": "start_time",
                    "interval": "day"
                },
                "aggs": {
                    "message_count": {
                        "sum": {
                            "field": "message_count"
                        }
                    },
                    "duration": {
                        "sum": {
                            "field": "duration"
                        }
                    }
                }
            }
        }
    })

    results = [
        {
            "datetime": item["key_as_string"][:10],
            "session_count": item["doc_count"],
            "message_count": item["message_count"]["value"],
            "total_duration": item["duration"]["value"],
        }
        for item in data["aggregations"]["session"]["buckets"]
    ]

    return Response(json.dumps(results), mimetype="application/json")


def aggregation(criteria, value):
    data = search({
        "size": 0,
        "query": {
            "match": {
                criteria: value
            }
        },
        "aggs": {
            "hit_id": {
                "terms": {
                    "field": "hit_id.keyword"
                }
            },
            "assignment_id": {
                "terms": {
                    "field": "assignment_id.keyword"
                }
            },
            "ip_address": {
                "terms": {
                    "field": "ip_address.keyword"
                }
            },
            "fingerprint": {
                "terms": {
                    "field": "fingerprint"
                }
            }
        }
    })

    results = {}
    for aggs in ("hit_id", "assignment_id", "ip_address", "fingerprint"):
        if len(data["aggregations"][aggs]["buckets"]) > 0:
            results[aggs] = data["aggregations"][aggs]["buckets"]

    return Response(json.dumps(results), mimetype="application/json")


# Static Files
@app.route(api_prefix + "/analytics.js", methods=['GET'])
def analytics_js():
    return send_file('./js/analytics.js')


@app.route(api_prefix + "/analytics.css", methods=['GET'])
def analytics_css():
    return send_file('./css/analytics.css')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)

