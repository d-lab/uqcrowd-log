import sys
import json
from elasticsearch import Elasticsearch

index_prefix = "uqcrowd-log"

if __name__ == "__main__":

    file_name = sys.argv[1]
    es = Elasticsearch()

    data = es.search(index=index_prefix + "*", scroll='2m', size=1000)
    scroll_id = data['_scroll_id']
    total = data['hits']['total']
    hits = data['hits']['hits']
    count = 0
    with open(file_name, "w") as file:
        while len(hits) > 0:
            for hit in hits:
                file.write(json.dumps(hit["_source"]) + "\n")
                count += 1
            print("Exported", count, "of", total)
            data = es.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = data['_scroll_id']
            hits = data['hits']['hits']
