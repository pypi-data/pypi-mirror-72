from elasticapm import Client
from elasticapm.context.contextvars import execution_context
from elasticapm.utils.disttracing import TraceParent
from inspect import signature, Parameter, _KEYWORD_ONLY
from mlchain import mlconfig
from mlchain.base.converter import str2bool

class TraceApm:
    def __init__(self, name=None, trace=None):
        self.name = name or mlconfig.name
        if trace is None:
            trace = str2bool(mlconfig.trace)
        self.trace = trace
        if self.trace:
            self.client = Client(service_name=self.name)

    def __call__(self, func):
        def f(*args, __headers__=None, **kwargs):
            if __headers__ is None:
                __headers__ = {}
            if 'Traceparent' in __headers__:
                trace_parent = TraceParent.from_string(__headers__['Traceparent'])
            else:
                trace_parent = None
            name = str(func.__name__)
            if self.trace:
                self.client.begin_transaction(name, trace_parent=trace_parent)
            out = func(*args, **kwargs)
            if self.trace:
                self.client.end_transaction(name)
            return out

        func_signature = signature(func)
        parameters = tuple(func_signature.parameters.values()) + (
            Parameter('__headers__', kind=_KEYWORD_ONLY, default=None, annotation=dict),)
        f.__signature__ = func_signature.replace(parameters=parameters)
        f.__wrapper__ = True
        return f


def apm_header():
    transaction = execution_context.get_transaction()
    if transaction:
        return {'Traceparent': transaction.trace_parent.to_string()}
    else:
        return {}
