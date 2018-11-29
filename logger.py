from elasticsearch import Elasticsearch
from flask import Flask, request
import redis
import sys

api_prefix = "/logger/v1.0/"
index_name = "uqcrowd-log"

app = Flask(__name__)
es = Elasticsearch()
re = redis.Redis(host='localhost', port=6379, db=0)


@app.route(api_prefix + "redis", methods=['POST'])
def insert():
    re.lpush(index_name, request.data)
    return "True"


@app.route(api_prefix + "index", methods=['POST'])
def index():
    es.index(index=index_name, doc_type=index_name, body=request.data)
    return "True"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)
