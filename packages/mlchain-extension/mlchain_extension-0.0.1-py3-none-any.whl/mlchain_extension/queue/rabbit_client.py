import weakref
from uuid import uuid4
from mlchain.base.serializer import MsgpackSerializer, JsonParser
import pika
from pika.spec import BasicProperties
from mlchain.observe.apm import get_transaction
from mlchain.config import rabbit_config


class RabbitFunction:
    def __init__(self, connection_params, function_name, async_params=None, exchange=None, routing_key=None,
                 serializer=None, metadata_serializer=None):
        self.connect_params = connection_params
        self.function_name = function_name
        self.async_params = async_params or {}
        self.exchange = exchange
        self.routing_key = routing_key
        self.serializer = serializer
        self.metadata_serializer = metadata_serializer
        self.connection_ = None
        self.channel_ = None

    @property
    def channel(self):
        if self.channel_ is None:
            self.channel_ = self.connection.channel()
        return self.channel_

    @property
    def connection(self):
        if self.connection_ is None:
            self.connection_ = pika.BlockingConnection(self.connect_params)
        return self.connection_

    def __call__(self, *args, **kwargs):
        transaction = get_transaction()
        if transaction:
            Traceparent = transaction.trace_parent.to_string()
        else:
            Traceparent = None

        key = uuid4().hex
        async_params = self.async_params

        inputs = self.metadata_serializer.encode({
            'args': args,
            'kwargs': kwargs,
            'async_params': self.async_params
        })

        try:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key=self.routing_key,
                                       body=self.serializer.encode(inputs),
                                       properties=BasicProperties(message_id=key,
                                                                  priority=async_params.get('priority',
                                                                                            None),
                                                                  expiration=async_params.get('expiration',
                                                                                              None),
                                                                  headers={'Traceparent': Traceparent}),
                                       )

            return key
        except Exception as e:
            if self.connection_:
                self.connection_.close()
            self.connection_ = None
            self.channel_ = None
            return None


class RabbitAsyncFunction(RabbitFunction):
    async def __call__(self, *args, **kwargs):
        return RabbitFunction.__call__(self, *args, **kwargs)


class RabbitModel:
    def __init__(self, host, port, exchange=None, serializer=None, metadata_serializer=None, name='rabbit_client',
                 version='lastest',
                 check_status=False, input_queue={}, async_params={}):
        """
        Remote model
        :client: Client to communicate, which can not be None
        :name: Name of model
        :version: Version of model
        :check_status: Check model is exist or not, and get description of model
        """

        self.name = name
        self.version = version
        self.serializer = serializer
        self.metadata_serializer = metadata_serializer
        self.connect_params = pika.ConnectionParameters(host=host, port=port)
        self.async_params = async_params
        self.all_func_des = input_queue
        self.all_func_params = None
        self.all_attributes = None
        self.exchange = exchange
        self._cache = weakref.WeakValueDictionary()

    def _check_function(self, name):
        if self.all_func_des is not None:
            if name in self.all_func_des:
                return True
            else:
                return False
        else:
            return True

    def _check_attribute(self, name):
        if self.all_attributes is not None:
            if name in self.all_attributes:
                return True
            else:
                return False
        else:
            return True

    def __getattr__(self, name):
        if name in self._cache:
            true_function = self._cache[name]
        else:
            if not self._check_function(name):
                if not self._check_attribute(name) and not name.endswith('_async'):
                    raise AssertionError("This model has no method or attribute name = {0} or it hasnt been served. The only served is: \n\
                                          Functions: {1} \n\
                                          Attributes: {2}".format(name, list(self.all_func_des.keys()),
                                                                  list(self.all_attributes)))
                else:
                    return None

            else:
                true_function = RabbitFunction(self.connect_params, name, self.async_params, self.exchange,
                                               self.all_func_des[name], self.serializer, self.metadata_serializer)
            self._cache[name] = true_function

        return true_function

    def __eq__(self, other):
        return self.client is other.client and self.name == other.name and self.version == other.version

    def __hash__(self):
        return hash(self.client) + hash(self.name) + hash(self.version)


class RabbitAsyncModel(RabbitModel):
    def __getattr__(self, name):
        if name in self._cache:
            true_function = self._cache[name]
        else:
            if not self._check_function(name):
                if not self._check_attribute(name) and not name.endswith('_async'):
                    raise AssertionError("This model has no method or attribute name = {0} or it hasnt been served. The only served is: \n\
                                          Functions: {1} \n\
                                          Attributes: {2}".format(name, list(self.all_func_des.keys()),
                                                                  list(self.all_attributes)))
                else:
                    return None

            else:
                true_function = RabbitFunction(self.connect_params, name, self.async_params, self.exchange,
                                               self.all_func_des[name], self.serializer, self.metadata_serializer)
            self._cache[name] = true_function

        return true_function

    def __eq__(self, other):
        return self.client is other.client and self.name == other.name and self.version == other.version

    def __hash__(self):
        return hash(self.client) + hash(self.name) + hash(self.version)


class RabbitClient:
    """
    Mlchain Client Model Class
    """

    def __init__(self, host=None, port=None, input_queue=None, async_params=None):
        """
        Remote model
        :client: Client to communicate, which can not be None
        :name: Name of model
        :version: Version of model
        :check_status: Check model is exist or not, and get description of model
        """
        self.serializer = MsgpackSerializer()
        self.metadata_serializer = JsonParser()
        self.host = host or rabbit_config.HOST
        self.port = port or rabbit_config.PORT
        self.async_params = async_params
        self.input_queue = input_queue

    def model(self, name: str = "", version: str = "", check_status=True):
        return RabbitModel(host=self.host, port=self.port, exchange=name, serializer=self.serializer,
                           metadata_serializer=self.metadata_serializer,
                           name=name, version=version, check_status=check_status, async_params=self.async_params,
                           input_queue=self.input_queue)

    def async_model(self, name: str = "", version: str = "", check_status=True):
        return RabbitAsyncModel(host=self.host, port=self.port, exchange=name, serializer=self.serializer,
                                metadata_serializer=self.metadata_serializer,
                                name=name, version=version, check_status=check_status, async_params=self.async_params,
                                input_queue=self.input_queue)
