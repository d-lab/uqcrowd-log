from flask import Flask, request, Response, send_file
import json
import requests
import sys

app = Flask(__name__)
api_prefix = "/analytics"
base_uri = "http://localhost:9200/uqcrowd-session-*/_search"


@app.route(api_prefix + "/session/worker/<worker_id>", methods=['POST'])
def worker(worker_id):
    return search({
        "query": {
            "match": {
                "worker_id": worker_id
            }
        }
    })


@app.route(api_prefix + "/session/client/<fingerprint>", methods=['POST'])
def client(fingerprint):
    return search({
        "query": {
            "match": {
                "fingerprint": fingerprint
            }
        }
    })


def search(query):
    response = requests.get(base_uri, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    results = json.loads(response.text)
    sessions = [session['_source'] for session in results['hits']['hits']]
    return Response(json.dumps(sessions), mimetype="application/json")


@app.route(api_prefix + "/analytics.js", methods=['GET'])
def analytics_js():
    return send_file('./js/analytics.js')


@app.route(api_prefix + "/analytics.css", methods=['GET'])
def analytics_css():
    return send_file('./css/analytics.css')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)

