import time
import redis
import grequests
import requests
import threading
from collections import deque
from elasticsearch import Elasticsearch


# url = "http://dke-uqcrowd-log.uqcloud.net/logger/v1.0/index"
# url = 'http://localhost:5009/logger/redis'
url = 'http://localhost:5000/logger/index'

re = redis.Redis(host='localhost', port=6379, db=0)
es = Elasticsearch()
index_name = "uqcrowd-log"
count = 0


def enqueue(q, m):
    c = 0
    with open('./data/mturklog.jl') as f:
        for line in f:
            c += 1
            q.append(line.strip())
            if c == m:
                break


def elastic(q):
    while len(q) > 0:
        m = q.popleft()
        es.index(index=index_name, doc_type=index_name, body=m)
        # print(len(q))


def redis(q):
    while len(q) > 0:
        m = q.popleft()
        re.rpush(index_name, m)
        # print(len(q))


def post(q):
    while len(q) > 0:
        m = q.popleft()
        requests.post(url, data=m)
        # print(len(q))


def async_post(q):
    reqs = []
    while len(q) > 0:
        m = queue.popleft()
        reqs.append(grequests.get(url, hooks={'response': handler}))
    grequests.map(requests)


def handler(response, **kwargs):
    global count
    count += 1
    print(count, response, kwargs)
    response.close()


if __name__ == "__main__":
    queue = deque()
    enqueue(queue, 10000)
    concurrent = 30;
    start_time = time.time()
  
    threads = []

    for i in range(concurrent):
        t = threading.Thread(target=elastic, args=(queue,))
        # t = threading.Thread(target=redis, args=(queue,))
        # t = threading.Thread(target=post, args=(queue,))
        t.start()
        threads.append(t)

    for i in range(concurrent):
        threads[i].join()

    elapsed_time = time.time() - start_time

    print(elapsed_time)




