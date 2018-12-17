import json
import time
import redis
import requests
import threading
from collections import deque
from elasticsearch import Elasticsearch
from datetime import datetime

# logger_uri = "http://dke-uqcrowd-log.uqcloud.net/logger/v1.0/index"
logger_uri = 'http://localhost:5000/logger/index'

re = redis.Redis(host='localhost', port=6379, db=0)
es = Elasticsearch()
index_prefix = "uqcrowd-log"
date_shift = 190


def load_messages_from_file(file_path, queue, max_count):
    """ Load all the stored messages from file

    Parameters:
        file_path (string): The file that store all the message
        queue (deque): The reference to the queue which will store all the messages
        max_count (int): Maximum number of message to load
    """
    count = 0
    with open(file_path) as f:
        for line in f:
            count += 1
            queue.append(line.strip())
            if count == max_count:
                break


def send_to_elastic(queue):
    """ Send all the message from queue to local elasticsearch server

    Parameters:
        queue (deque): The reference to the queue which will store all the messages
    """
    while len(queue) > 0:
        message = json.loads(queue.popleft())
        index_name = index_prefix + "-" + datetime.now().strftime('%Y-%m-%d')
        es.index(index=index_name, doc_type=index_prefix, body=json.dumps(message))
        print(len(queue))


def send_to_redis(queue):
    """ Send all the message from queue to local redis cache server

    Parameters:
        queue (deque): The reference to the queue which will store all the messages
    """
    while len(queue) > 0:
        message = queue.popleft()
        re.rpush(index_prefix, message)
        print(len(queue))


def send_to_logger(queue, uri):
    """ Send all the message from queue to local redis cache server

    Parameters:
        queue (deque): The reference to the queue which will store all the messages
        uri (string: The uri of the logger server
    """
    while len(queue) > 0:
        message = queue.popleft()
        requests.post(uri, data=message)
        print(len(queue))


def main():
    queue = deque()
    threads = []

    # Number of message to send
    number_of_message = 30000

    # Number of concurrent process to send the messages
    number_of_threads = 8

    # Load all the messages from file to queue
    load_messages_from_file("./data/mturklog.jl", queue, number_of_message)

    start_time = time.time()

    # Start multi-threading processes
    for i in range(number_of_threads):

        # Initialize the thread (Choose one of three options)
        thread = threading.Thread(target=send_to_logger, args=(queue, logger_uri))
        # thread = threading.Thread(target=send_to_elastic, args=(queue,))
        # thread = threading.Thread(target=send_to_redis, args=(queue,))

        # Start the thread and append it to the thread list for managing
        thread.start()
        threads.append(thread)

    # Join all the thread together so all the thread will be terminated at same time when all the jobs a finished.
    for i in range(number_of_threads):
        threads[i].join()

    # Calculate and print elapsed time
    elapsed_time = time.time() - start_time
    print(elapsed_time)


if __name__ == "__main__":
    main()




