from mlchain.base.serve_model import ServeModel
from concurrent import futures
from .base import MLServer
from mlchain.base.log import format_exc
import grpc
from .protos import mlchain_pb2, mlchain_pb2_grpc
from mlchain.observe import apm
from threading import Thread
from mlchain.config import apm_config
import time
import random
import mlchain

class GrpcServer(mlchain_pb2_grpc.MLChainServiceServicer, MLServer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, model: ServeModel, name=None, trace=False, monitor_sampling_rate=0.0, api_keys=None,version = '0.0'):
        MLServer.__init__(self, model, name=name)
        self.apm = apm.Client(config=apm_config, service_name=self.name) if trace else None
        self.logger = None
        self.monitor_sampling_rate = monitor_sampling_rate
        self.version = version

    def get_serializer(self, serializer):
        if serializer in self.serializers_dict:
            return self.serializers_dict[serializer]
        else:
            return self.serializers_dict['application/json']
    def ping(self, request, context):
        return mlchain_pb2.Byte(value=b'pong')
    def call(self, request, context):
        header = request.header
        function_name = request.function_name
        args = request.args
        kwargs = request.kwargs
        serializer = self.get_serializer(header.serializer)
        headers = request.headers

        if self.apm and header.Traceparent:
            trace_parent = apm.TraceParent.from_string(header.Traceparent)
        else:
            trace_parent = None
        log = (random.random() < self.monitor_sampling_rate or trace_parent is not None)
        id = None
        if self.apm and log:
            transaction = self.apm.begin_transaction(str(function_name), trace_parent=trace_parent)
            if transaction:
                id = transaction.id
        info = {}
        args = serializer.decode(args)
        kwargs = serializer.decode(kwargs)
        func = self.model.get_function(function_name)
        kwargs = self.get_kwargs(func, *args, **kwargs)
        kwargs = self._normalize_kwargs_to_valid_format(kwargs, func)
        if '__headers__' in kwargs:
            headers = kwargs.pop('__headers__')
        try:
            start = time.time()
            output = self.model.call_function(function_name, None,__headers__ = headers, **kwargs)
            duration = time.time() - start
            info["time"] = duration
            if self.apm and log:
                self.apm.end_transaction(str(function_name), result="done")

            if self.logger and log:
                self.logger.log(info, id=id, function_name=function_name, **kwargs)
            output = {
                'output': output,
                'time': duration,
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }

        except Exception as ex:
            if self.apm and log:
                self.apm.capture_exception()
                self.apm.end_transaction(self.name, result="error")
            info['error'] = True
            info['time'] = 0
            if self.logger and log:
                self.logger.log(info, id=id, function_name=str(function_name), **kwargs)
            output = {
                'output': str(ex),
                'time': 0,
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
        return mlchain_pb2.Output(output=serializer.encode(output))
    def run(self, host='127.0.0.1', port=10010, workers=1, block=True):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
        mlchain_pb2_grpc.add_MLChainServiceServicer_to_server(self, server)
        server.add_insecure_port('{0}:{1}'.format(host, port))
        server.start()
        if block:
            server.wait_for_termination()
        else:
            Thread(target=server.wait_for_termination).start()
