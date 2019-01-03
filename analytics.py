from flask import Flask, request, Response, send_file
import json
import requests
import sys

app = Flask(__name__)
api_prefix = "/analytics/"
base_uri = "http://localhost:9200"


@app.route(api_prefix + "session-count", methods=['GET'])
def session_count():
    uri = base_uri + "/uqcrowd-session-*/_search"
    worker_id = request.args.get('id')
    query = {
        "query": {
            "match": {
                "worker_id": worker_id
            }
        }
    }
    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    results = json.loads(response.text)
    sessions = [session['_source'] for session in results['hits']['hits']]
    return Response(json.dumps(sessions), mimetype="application/json")


@app.route(api_prefix + "message-count", methods=['GET'])
def message_count():
    uri = base_uri + "/uqcrowd-log-*/_search"
    worker_id = request.args.get('worker_id')
    query = {
        "size": 0,
        "aggs": {
            "daily_message_count": {
                "date_histogram": {
                    "field": "server_time",
                    "interval": "day"
                }
            }
        }
    }

    if worker_id:
        query["query"] = {
            "match": {
                "worker_id": worker_id
            }
        }

    response = requests.get(uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    results = json.loads(response.text)
    results = [[item["key_as_string"][:10], item["doc_count"]]
               for item in results["aggregations"]["daily_message_count"]["buckets"]]
    return Response(json.dumps(results), mimetype="application/json")


@app.route(api_prefix + "/analytics.js", methods=['GET'])
def analytics_js():
    return send_file('./js/analytics.js')


@app.route(api_prefix + "/analytics.css", methods=['GET'])
def analytics_js():
    return send_file('./js/analytics.css')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)

