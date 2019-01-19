import sys
import json
from elasticsearch import Elasticsearch

index_prefix = "uqcrowd-log"

if __name__ == "__main__":

    file_name = sys.argv[1]
    es = Elasticsearch()

    with open(file_name) as file:
        lines = file.readlines()

    total = len(lines)
    count = 0
    for line in lines:
        if count % 1000 == 0:
            print("Imported", count, "of", total)
        source = json.loads(line)
        index_name = index_prefix + "-" + source["server_time"][:10]
        es.index(index=index_name, doc_type=index_prefix, body=json.dumps(source))
        count += 1

