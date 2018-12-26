from elasticsearch import Elasticsearch
from flask import Flask, request
from datetime import datetime
import redis
import sys
import json

api_prefix = "/logger"
index_prefix = "uqcrowd-log"

app = Flask(__name__)
es = Elasticsearch()
re = redis.Redis(host='localhost', port=6379, db=0)

cache_mode = False


@app.route(api_prefix + "/insert", methods=['POST'])
def index():
    """ Receive POST request and store the message to redis or elasticsearch depends on cached mode """
    global cache_mode

    if cache_mode:
        # If using cache enabled, insert the message to redis server
        re.lpush(index_prefix, request.data)

    else:
        # Else send directly to the elasticsearch
        # The messages are indexed to indexes separated by date stamp
        index_name = index_prefix + "-" + datetime.now().strftime('%Y-%m-%d')

        # Add server time attribute
        message = json.loads(request.data)
        message['server_time'] = datetime.now().isoformat()

        # Insert to elasticsearch
        es.index(index=index_name, doc_type=index_prefix, body=json.dumps(message))

    return "True"


if __name__ == '__main__':
    # Check commandline arguments
    if len(sys.argv) < 2:
        print("ERROR! Missing Argument!")
        print("Usage:", sys.argv[0], "<Listening Port>")
        print("Example:", sys.argv[0], "5001")
    else:
        # Start the server with the listening port passed from commandline
        app.run(host='0.0.0.0', port=sys.argv[1], debug=False)
