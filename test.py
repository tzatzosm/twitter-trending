import json
from index.index import Indexer

json_obj = json.loads("{\"name\": \"marsel\"}")

indexer = Indexer('index_name', 'doc_type')
indexer.index(json_obj, 1)
