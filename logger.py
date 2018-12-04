from elasticsearch import Elasticsearch
from flask import Flask, request
from datetime import datetime
import redis
import sys

api_prefix = "/logger/"
index_prefix = "uqcrowd-log"

app = Flask(__name__)
es = Elasticsearch()
re = redis.Redis(host='localhost', port=6379, db=0)


@app.route(api_prefix + "enqueue", methods=['POST'])
def insert():
    re.lpush(index_prefix, request.data)
    return "True"


@app.route(api_prefix + "index", methods=['POST'])
def index():
    index_name = index_prefix + "-" + datetime.now().strftime('%Y-%m-%d')
    es.index(index=index_name, doc_type=index_prefix, body=request.data)
    return "True"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)
