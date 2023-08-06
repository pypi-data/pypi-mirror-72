from .base import QueueModel
from mlchain.base.serializer import MsgpackSerializer
import redis
import time
from bson.objectid import ObjectId
from threading import Thread
import logging


class RedisDatabase:
    def __init__(self, host=None, port=None, db=None, password=None, prefix='database', serializer=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client_ = None
        self.prefix = prefix
        self.serializer = serializer

    @property
    def client(self):
        if self.client_ is None or self:
            self.client_ = redis.Redis(host=self.host,
                                       port=self.port,
                                       password=self.password,
                                       db=self.db)
        return self.client_

    def insert(self, document, id=None, **kwargs):
        if id is None:
            id = ObjectId().__str__()
        for k, v in document.items():
            self.client.set('{0}_{1}_{2}'.format(self.prefix, id, k), self.serializer.encode(v))

    def get(self, id, *args, **kwargs):
        prefix = '{0}_{1}_*'.format(self.prefix, id)
        doc = {}
        for key in self.client.scan_iter(prefix, count=None):
            field = key.decode()[len(prefix) - 1:]
            v = self.client.get(key)
            if v is not None:
                doc[field] = self.serializer.decode(v)
            else:
                doc[field] = None
        return doc

    def update(self, id, document, *args, **kwargs):
        for k, v in document.items():
            self.client.set('{0}_{1}_{2}'.format(self.prefix, id, k), self.serializer.encode(v))


class RedisQueue(QueueModel):
    def __init__(self, model, host=None, port=None, db=None, password=None,
                 deny_all_function=False,
                 blacklist=[], whitelist=[], version='0.0', name='MLChain',
                 input_queue=None, output_queue=None, retry=1):
        QueueModel.__init__(self, model, deny_all_function, blacklist, whitelist)

        self.serializer = MsgpackSerializer()
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
        print('listen queue', self.input_queue)
        print('response queue', self.output_queue)
        self.running = None
        self.retry = retry

    @property
    def client(self):
        if self.client_ is None or self:
            self.client_ = redis.Redis(host=self.host,
                                       port=self.port,
                                       password=self.password,
                                       db=self.db)
        return self.client_

    def callback(self, msg):
        function_name = msg['function_name']
        key = msg['uid']

        if key is None:
            key = str(ObjectId())
        self.database.update(id=key, document={'status': 'PROCESSING'})
        data = msg['data']
        args, kwargs = self.get_params(data)
        __headers__ = data.get('__headers__', {})
        try:
            start = time.time()
            output = self.call_function(function_name, key, __headers__, *args, **kwargs)
            self.database.update(id=key, document={'status': 'SUCCESS', 'output': output,
                                                   'time': time.time() - start})
        except Exception as e:
            logging.error(str(e))
            self.database.update(id=key, document={'status': 'RETRY'})
            if __headers__ is None:
                __headers__ = {}

            if 'RETRY' not in __headers__:
                __headers__['RETRY'] = self.retry
            if __headers__['RETRY'] > 0:
                __headers__['RETRY'] -= 1
                self.call_async(function_name, key, __headers__, *args, **kwargs)
            return

    def call_async(self, function_name_, key_=None, __headers__=None, *args, **kwargs):
        function_name, key = function_name_, key_
        if __headers__ is None:
            __headers__ = {}
        if key is None:
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
            self.client.rpush(self.input_queue, self.serializer.encode({
                'data': inputs,
                'uid': key,
                'function_name': function_name
            }))

            return key
        except Exception as e:
            logging.error(str(e))
            self.database.update(id=key, document={'status': 'FAILURE'})
            return None

    def get_params(self, value):
        return value.get('args', []), value.get('kwargs', {})

    def response_function(self, key, output):
        pass

    def result(self, key):
        output = self.database.get(id=key)
        if output:
            return {'status': output.get('status'), 'output': output.get('output'), 'time': output.get('time', 0)}
        return {'status': None, 'output': None, 'time': 0}

    def run(self, threading=False):
        self.running = True
        self.threat = None
        if not threading:
            self.background()
        else:
            if self.threat is None:
                self.threat = Thread(target=self.background)
                self.threat.start()
            elif not self.threat.is_alive():
                self.threat = Thread(target=self.background)
                self.threat.start()

    def background(self):
        while self.running:
            while self.running:
                try:
                    msg = self.client.lpop(self.input_queue)
                    if msg is None:
                        time.sleep(0.1)
                        continue
                    msg = self.serializer.decode(msg)
                    self.callback(msg)
                except Exception as e:
                    logging.error(str(e))
                    self.client_ = None
                    time.sleep(1)
                    break
