from flask import Flask, request, Response
import json
import requests
import sys

app = Flask(__name__)
api_prefix = "/analytics/"
base_uri = "http://localhost:9200"


@app.route(api_prefix + "session/worker", methods=['GET'])
def get_sessions_by_worker_id():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)

