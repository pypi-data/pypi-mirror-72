from mlchain import mlconfig
from .grpc_model import GrpcModel
from .http_model import HttpModel


class HttpClient:
    def __init__(self, api_key=None, api_address=None, serializer='json', timeout=5 * 60, headers=None):
        self.api_key = api_key
        self.api_address = api_address
        self.serializer = serializer
        self.timeout = timeout
        self.headers = headers

    def model(self, name: str = "", version: str = "", check_status=True):
        return HttpModel(api_key=self.api_key, api_address=self.api_address, serializer=self.serializer,
                         timeout=self.timeout, headers=self.headers, name=name, version=version,
                         check_status=check_status)

class GrpcClient:
    def __init__(self, api_key=None, api_address=None, serializer='json', timeout=5 * 60, headers=None):
        self.api_key = api_key
        self.api_address = api_address
        self.serializer = serializer
        self.timeout = timeout
        self.headers = headers

    def model(self, name: str = "", version: str = "", check_status=True):
        return GrpcModel(api_key=self.api_key, api_address=self.api_address, serializer=self.serializer,
                         timeout=self.timeout, headers=self.headers, name=name, version=version,
                         check_status=check_status)


def get_model(name):
    config = mlconfig.get_client_config(name)
    timeout = config.timeout
    if timeout is not None:
        try:
            timeout = int(timeout)
        except:
            raise ValueError("timeout must be an integer")
    client_type = mlconfig.type or 'http'
    if client_type == 'http':
        return HttpClient(api_key=config.api_key, api_address=config.api_address,
                          serializer=config.serializer or 'json', timeout=timeout).model(
            check_status=bool(config.check_status))
    elif client_type == 'grpc':
        return GrpcClient(api_address=config.api_address,
                          serializer=config.serializer or 'json').model(check_status=bool(config.check_status))
    else:
        raise ValueError("Client type must be http or grpc")
