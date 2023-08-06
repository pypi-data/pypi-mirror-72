from mlchain.rpc.client.base import MLClient
from .redis_queue import RedisDatabase
import time
from bson.objectid import ObjectId
import logging
import redis

class RedisModel(MLClient):
    def __init__(self, host=None, port=None, db=None, password=None, version='0.0', name='MLChain',
                 input_queue=None, output_queue=None, check_status=False, headers=None, **kwargs):
        MLClient.__init__(self, api_key=None, api_address=None, serializer='msgpack', name=name,
                          version=version, check_status=check_status, headers=headers, **kwargs)
        print(self.serializer)
        self.host = host or 'localhost'
        self.port = port or 6379
        self.db = db or 0
        self.password = password or ''
        self.client_ = None
        prefix = []
        self.version = version
        self.name = name
        prefix.append(name)
        prefix.append(version)
        self.output_queue = output_queue or '.'.join(prefix + ['output'])
        self.input_queue = input_queue or '.'.join(prefix + ['input'])

        self.database = RedisDatabase(host=self.host, port=self.port, db=self.db, password=self.password,
                                      prefix='{0}-{1}'.format('inference', self.name).lower(),
                                      serializer=self.serializer)

    @property
    def client(self):
        if self.client_ is None or self:
            self.client_ = redis.Redis(host=self.host,
                                       port=self.port,
                                       password=self.password,
                                       db=self.db)
        return self.client_
    def _get(self, api_name, headers=None, params=None):
        """
        GET data from url
        """
        pass

    def _post(self, function_name, headers=None, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if headers is None:
            headers = {}
        __headers__ = headers
        key = str(ObjectId())
        timestamp = int(time.time())
        timezone = time.timezone

        inputs = {
            'args': args,
            'kwargs': kwargs,
            '__headers__': __headers__
        }

        self.database.insert(id=key, document={'status': 'PENDING',
                                               'uid': key,
                                               'timestamp': timestamp,
                                               'timezone': timezone,
                                               'function': function_name,
                                               'version': self.version,
                                               '__headers__': __headers__,
                                               'input': inputs
                                               })
        try:
            print(self.serializer)
            self.client.rpush(self.input_queue, self.serializer.encode({
                'data': inputs,
                'uid': key,
                'function_name': function_name
            }))

            return self.serializer.encode({'output':key})
        except Exception as e:
            logging.error(str(e))
            self.database.update(id=key, document={'status': 'FAILURE'})
            return self.serializer.encode({'output':None})

    def result(self, key):
        output = self.database.get(id=key)
        if output:
            return {'status': output.get('status'), 'output': output.get('output'), 'time': output.get('time', 0)}
        return {'status': None, 'output': None, 'time': 0}

    def _get_function(self, name):
        if name == 'store_get':
            return self.result
        else:
            return MLClient._get_function(self, name)
