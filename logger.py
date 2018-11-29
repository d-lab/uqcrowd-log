from __future__ import print_function
import json, sys
from elasticsearch import Elasticsearch
from flask import Flask, request
import redis

prefix = "/logger/v1.0/"

app = Flask(__name__)
es = Elasticsearch()
re = redis.Redis(host='localhost', port=6379, db=0)
count = 0

@app.route(prefix + "redis", methods=['POST'])
def insert():
    try:
        re.lpush('uqcrowd-log', request.data)
        return "{success: True}"
    except Exception as ex:
        return ""


@app.route(prefix + "index", methods=['POST'])
def index():
    global count
    count += 1
    print(request.data, file=sys.stdout)
    es.index(index="uqcrowd-log", doc_type="uqcrowd-log", body=request.data)
    return "{success: True}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=False)
