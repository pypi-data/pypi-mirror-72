from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from .base import MLDatabase
from mlchain.config import elastic_search_config
import json


def encode(data):
    if isinstance(data, (dict, list)):
        return {'type': 'json', 'data': json.dumps(data, ensure_ascii=False)}
    elif isinstance(data, (int, float)):
        return {'type': 'numeric', 'value': data}
    elif isinstance(data, str):
        return {'type': 'string', 'data': data}
    elif isinstance(data, (type(None))):
        return {'type': 'none'}
    else:
        return data


def decode(data):
    if isinstance(data, dict):
        data_type = data.get('type', None)
        if data_type == 'json':
            return json.loads(data['data'])
        elif data_type == 'string':
            return data['data']
        elif data_type == 'numeric':
            return data['value']
        elif data_type == 'none':
            return None
        else:
            return data
    else:
        return data


class ESDatabase(MLDatabase):
    def __init__(self, client=None, host=None, port=None, default_index=None):
        self.client_ = client
        self.host = host or elastic_search_config.HOST
        self.port = port or elastic_search_config.PORT
        self.default_index = default_index

    @property
    def client(self):
        if self.client_ is None:
            self.client_ = Elasticsearch([{'host': self.host, 'port': self.port}])

        return self.client_

    def get_index(self, index=None):
        index = index or self.default_index

        if not self.client.indices.exists(index):
            settings = {
                "number_of_shards": 5,
                "number_of_replicas": 1,
                "blocks": {
                    "read_only_allow_delete": False
                }
            }
            body = {'settings': settings}
            self.client.indices.create(index=index, body=body)

        return index

    def insert(self, document, id=None, doc_type='random_type', index=None):
        index = self.get_index(index)
        document = {k: encode(v) for k, v in document.items()}
        try:
            res = self.client.index(index=index, doc_type=doc_type, body=document, id=id)
            return res
        except:
            self.client_ = None
            return None

    def get(self, id, index=None):
        index = self.get_index(index)
        try:
            document = self.client.get_source(index=index, id=id)
        except Exception as e:
            document = None
        if document:
            document = {k: decode(v) for k, v in document.items()}
        return document

    def update(self, id, document, index=None):
        index = self.get_index(index)
        document = {k: encode(v) for k, v in document.items()}
        try:
            self.client.update(index, id, body={'doc': document})
            return True
        except NotFoundError:
            self.client.index(index, body=document, id=id)
        except Exception as e:
            print(e)
            self.client_ = None
            return False
