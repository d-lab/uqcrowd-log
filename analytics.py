from flask import Flask, request, Response, send_file
import json
import requests
import sys

app = Flask(__name__)
api_prefix = "/analytics"
base_uri = "http://localhost:9200/uqcrowd-session-*/_search"


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


@app.route(api_prefix + "/session/worker/<worker_id>/session_count", methods=['GET'])
def worker_message_count(worker_id):
    data = search({
        "size": 0,
        "query": {
            "match": {
                "worker_id": worker_id
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

    rows = []
    for item in data["aggregations"]["session"]["buckets"]:
        row = {
            "c": [
                {"v": item["key_as_string"][:10]},
                {"v": item["doc_count"]},
                {"v": item["duration"]["value"]},
                {"v": item["message_count"]["value"]}
            ]
        }
        rows.append(row)

    results = {
        "cols": [
            {"label": "Date", "type": "date"},
            {"label": "Session Count", "type": "number"},
            {"label": "Message Count", "type": "number"},
            {"label": "Total Duration", "type": "number"}
        ],
        "rows": rows
    }

    return Response(json.dumps(results), mimetype="application/json")


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


def search(query):
    response = requests.get(base_uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    return json.loads(response.text)


@app.route(api_prefix + "/analytics.js", methods=['GET'])
def analytics_js():
    return send_file('./js/analytics.js')


@app.route(api_prefix + "/analytics.css", methods=['GET'])
def analytics_css():
    return send_file('./css/analytics.css')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)

