from .base import QueueModel
from mlchain.base.serializer import MsgpackSerializer, JsonParser
import pika
from pika.spec import BasicProperties
import time
from mlchain_extension.storage import MLStorage
from mlchain_extension.database import MLDatabase
from mlchain_extension.storage.object_storage import ObjectStorage
from mlchain_extension.database.elastic_search import ESDatabase
import requests
from bson.objectid import ObjectId
from threading import Thread
import logging


class RabbitQueue(QueueModel):
    def __init__(self, model, host=None, port=None, module_name='queueserver', deny_all_function=False,
                 blacklist=[], whitelist=[], org_name=None, version='0.0',
                 project_name=None, storage: MLStorage = None, database: MLDatabase = None, trace=False,
                 input_queue=None, output_queue=None, retry=1):
        QueueModel.__init__(self, model, deny_all_function, blacklist, whitelist)

        self.serializer = MsgpackSerializer()
        self.metadata_serializer = JsonParser(storage or ObjectStorage(), prefix=self.name + '/serializer/')
        self.host = host
        self.port = port
        prefix = []
        self.org_name = org_name
        self.project_name = project_name
        self.version = version
        if org_name is not None:
            prefix.append(org_name)
        if project_name is not None:
            prefix.append(project_name)
        prefix.append(module_name)
        prefix.append(version)
        self.output_queue = output_queue or '.'.join(prefix + ['output'])
        self.input_queue = input_queue or {function_name: '.'.join(prefix + ['call', function_name])
                                           for function_name in self.all_serve_function}
        self.module_name = module_name

        self.public_channel = self.get_channel()
        self.output_channel = self.get_channel()

        self.queue = '.'.join(prefix)

        self.queue2function = {v: k for k, v in self.input_queue.items()}
        self.database = database or ESDatabase(default_index='{0}-{1}'.format('inference', module_name).lower())
        print('listen queue', self.input_queue)
        print('response queue', self.output_queue)
        self.running = None
        self.retry = retry

    def get_channel(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port)).channel()

    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))

    def callback(self, ch, method, properties, body):
        queue_name = method.routing_key
        if queue_name in self.queue2function:
            function_name = self.queue2function[queue_name]
            key = properties.message_id
            headers = properties.headers

            if key is None:
                key = str(ObjectId())
            self.database.update(id=key, document={'status': 'PROCESSING'})
            data = self.serializer.decode(body)
            data = self.metadata_serializer.decode(data)
            args, kwargs = self.get_params(data)
            async_params = data.get('async_params', {})
            try:
                start = time.time()

                output = self.call_function(function_name, key, *args, **kwargs)
                output_string = self.metadata_serializer.encode(output)
                output_json = output_string  # json.loads(output_string)
                self.database.update(id=key, document={'status': 'SUCCESS', 'output': output_string,
                                                       'time': time.time() - start})
                return_api = async_params.get('return_api', None)
                if return_api:
                    try:
                        requests.post(return_api, json=output_json)
                    except:
                        pass
            except Exception as e:
                logging.error(str(e))
                self.database.update(id=key, document={'status': 'RETRY'})
                if async_params is None:
                    async_params = {}

                if 'RETRY' not in async_params:
                    async_params['RETRY'] = 0
                if async_params['RETRY'] < self.retry:
                    async_params['RETRY'] += 1
                    self.call_async(function_name, key, async_params, *args, **kwargs)
                return
        else:
            return

    def call_async(self, function_name_, key_=None, async_params_=None, *args, **kwargs):
        function_name, key, async_params = function_name_, key_, async_params_
        if function_name in self.input_queue:
            if async_params is None:
                async_params = {}
            if key is None:
                key = str(ObjectId())
            timestamp = int(time.time())
            timezone = time.timezone

            inputs = self.metadata_serializer.encode({
                'args': args,
                'kwargs': kwargs,
                'async_params': async_params
            })

            self.database.insert(id=key, document={'status': 'PENDING',
                                                   'uid': key,
                                                   'timestamp': timestamp,
                                                   'timezone': timezone,
                                                   'function': function_name,
                                                   'org': self.org_name,
                                                   'project': self.project_name,
                                                   'module': self.module_name,
                                                   'version': self.version,
                                                   'async_params': async_params,
                                                   'input': inputs
                                                   })
            try:
                self.public_channel.basic_publish(exchange=self.module_name,
                                                  routing_key=self.input_queue[function_name],
                                                  body=self.serializer.encode(inputs),
                                                  properties=BasicProperties(message_id=key,
                                                                             priority=async_params.get('priority',
                                                                                                       None),
                                                                             expiration=async_params.get('expiration',
                                                                                                         None)),
                                                  )

                return key
            except Exception as e:
                logging.error(str(e))
                self.database.update(id=key, document={'status': 'FAILURE'})
                if self.public_channel.is_closed:
                    self.public_channel = self.get_channel()
                return None
        else:
            return None

    def get_params(self, value):
        return value.get('args', []), value.get('kwargs', {})

    def response_function(self, key, output):
        self.output_channel.basic_publish(exchange=self.module_name,
                                          routing_key=self.output_queue,
                                          body=self.serializer.encode(output),
                                          properties=BasicProperties(message_id=key))

    def result(self, key):
        output = self.database.get(id=key)
        if output:
            if output['status'] == 'SUCCESS':
                output['output'] = self.metadata_serializer.decode(output['output'])
            return {'status': output.get('status'), 'output': output.get('output'), 'time': output.get('time', 0)}
        return {'status': None, 'output': None, 'time': 0}

    def start_consuming(self):
        while True:
            try:
                connection = self.get_connection()
                channel = connection.channel()
            except:
                time.sleep(1)
                continue
            self.consumer_channel = channel
            self.consumer_channel.exchange_declare(exchange=self.module_name, exchange_type='fanout')
            result = self.consumer_channel.queue_declare(self.queue, exclusive=False)
            queue_name = result.method.queue
            self.consumer_channel.queue_bind(exchange=self.module_name, queue=queue_name)
            self.consumer_channel.basic_consume(
                queue=self.queue, on_message_callback=self.callback, auto_ack=True, exclusive=False,
                consumer_tag=self.queue)
            try:
                channel.start_consuming()
            except pika.exceptions.ConnectionClosed:
                time.sleep(1)
                continue
            except KeyboardInterrupt:
                channel.stop_consuming()
            except Exception as e:
                print(e)
                continue
            try:
                connection.close()
            except:
                pass
            break

    def run(self, threading=False):
        if not threading:
            self.start_consuming()
        else:
            if self.running is None:
                self.running = Thread(target=self.start_consuming)
                self.running.start()
            elif not self.running.is_alive():
                self.running = Thread(target=self.start_consuming)
                self.running.start()
