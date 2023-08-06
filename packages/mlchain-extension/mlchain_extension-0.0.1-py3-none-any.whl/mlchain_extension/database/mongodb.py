from .base import MLDatabase
from pymongo.mongo_client import MongoClient


class MongoDatabase(MLDatabase):
    def __init__(self, client=None, host=None,
                 port=None,
                 document_class=dict,
                 tz_aware=None,
                 connect=None,
                 default_database = None,
                 default_collection = None,
                 **kwargs):
        if client is None:
            client = MongoClient(host=host, port=port, document_class=document_class, tz_aware=tz_aware,
                                 connect=connect, **kwargs)
        self.client = client
        self.default_database = default_database
        self.default_collection = default_collection

    def get_default(self, database=None, collection=None):
        return database or self.default_database, collection or self.default_collection

    def insert(self, document, id=None, database=None, collection=None):
        database, collection = self.get_default(database, collection)
        if id is not None:
            document['_id'] = id
        return self.client[database][collection].insert_one(document).inserted_id

    def get(self, id, database=None, collection=None):
        database, collection = self.get_default(database, collection)
        result = self.client[database][collection].find_one({'_id': id})
        if result:
            result.pop('_id')
        return result

    def update(self, id, document, database=None, collection=None):
        database, collection = self.get_default(database, collection)
        document['_id'] = id
        self.client[database][collection].find_one_and_update({'_id': id}, {'$set': document}, upsert=True,
                                                              projection=['_id'])
        return True
