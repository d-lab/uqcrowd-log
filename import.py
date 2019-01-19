import sys
import json
from elasticsearch import Elasticsearch

index_prefix = "uqcrowd-log"

if __name__ == "__main__":

    file_name = sys.argv[1]
    es = Elasticsearch()

    with open(file_name) as file:
        data = json.load(file)

    hits = data.get("hits").get("hits")
    sources = [hit.get("_source") for hit in hits]

    for source in sources:
        print(source)
        index_name = index_prefix + "-" + source["server_time"][:10]
        es.index(index=index_name, doc_type=index_prefix, body=json.dumps(source))
