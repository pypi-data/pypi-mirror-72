from mlchain.base.serve_model import ServeModel
from mlchain.base.log import logger,format_exc
from quart_cors import cors as CORS
from quart import Quart, request, Response,jsonify,render_template,Blueprint,send_from_directory
from quart.exceptions import RequestEntityTooLarge
from collections import defaultdict
from .base import MLServer,Converter
from mlchain.observe import apm
from mlchain.base.wrapper import GunicornWrapper, HypercornWrapper
import sys
import inspect
from quart.datastructures import FileStorage
from mlchain.config import apm_config
import time
import random
import re
import mlchain
from mlchain.base.exceptions import MlChainError,MLChainAssertionError
from .swagger import SwaggerTemplate
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'server/templates')
STATIC_PATH = os.path.join(APP_PATH, 'server/static')

class QuartEndpointAction(object):
    """
    Defines an Quart Endpoint for a specific action for any client.
    """

    def __init__(self, action, serializers_dict, dump_request=None, version='latest',api_keys = None):
        """
        Create the endpoint by specifying which action we want the endpoint to perform, at each call
        :param action: The function to execute on endpoint call
        """
        # Defines which action (which function) should be called
        assert callable(action)

        self.action = action
        self.serializers_dict = serializers_dict
        self.dump_request = dump_request
        self.version = version
        self.json_serializer = self.serializers_dict['application/json']
        self.msgpack_serializer = self.serializers_dict['application/msgpack']
        self.msgpack_blosc_serializer = self.serializers_dict['application/msgpack_blosc']
        self.api_keys = api_keys

    async def __get_json_response(self, output, status=200):
        """
        Get JSON Reponse
        """
        output_encoded = self.json_serializer.encode(output)
        return Response(output_encoded, mimetype='application/json', status=status)

    async def __get_msgpack_response(self, output, status=200):
        """
        Get msgpack Reponse
        """
        output_encoded = self.msgpack_serializer.encode(output)
        return Response(output_encoded, mimetype='application/msgpack', status=status)

    async def __get_msgpack_blosc_response(self, output, status=200):
        """
        Get msgpack blosc response
        """
        output_encoded = self.msgpack_blosc_serializer.encode(output)
        return Response(output_encoded, mimetype='application/msgpack_blosc', status=status)

    async def __call__(self, *args, **kwargs):
        """
        Standard method that effectively perform the stored action of this endpoint.
        :param args: Arguments to give to the stored function
        :param kwargs: Keywords Arguments to give to the stored function
        :return: The response, which is a jsonified version of the function returned value
        """
        start_time = time.time()

        # If data POST is in msgpack format
        content_type = request.content_type
        if content_type not in self.serializers_dict:
            headers = {k.upper(): v for k, v in request.headers.items()}
            'SERIALIZER'
            if 'SERIALIZER'.upper() in headers:
                content_type = headers['SERIALIZER']
            else:
                content_type = 'application/json'

        serializer = self.serializers_dict.get(content_type, self.serializers_dict['application/json'])
        if content_type == 'application/msgpack':
            response_function = self.__get_msgpack_response
        elif content_type == 'application/msgpack_blosc':
            response_function = self.__get_msgpack_blosc_response
        else:
            response_function = self.__get_json_response
        if request.method == 'POST' and self.api_keys is not None or (isinstance(self.api_keys,(list,dict)) and len(self.api_keys) >0):
            authorized = False
            has_key = False
            for key in ['x-api-key','apikey','apiKey','api-key']:
                apikey = request.headers.get(key,'')
                if apikey != '':
                    has_key = True
                if apikey in self.api_keys:
                    authorized = True
                    break
            if not authorized:
                if has_key:
                    error = 'Unauthorized. Api-key incorrect.'
                else:
                    error = 'Unauthorized. Lack of x-api-key or apikey or api-key in headers.'
                output = {
                    'error':error,
                    'api_version':self.version,
                    'mlchain_version':mlchain.__version__
                }
                return await response_function(output,401)
        try:
            # Perform the action
            if inspect.iscoroutinefunction(self.action) or (not inspect.isfunction(self.action) and hasattr(self.action,
                                                                                                            '__call__') and inspect.iscoroutinefunction(
                self.action.__call__)):
                if request.method == 'POST':
                    output = await self.action(*args, **kwargs, serializer=serializer)
                else:
                    output = await self.action(*args, **kwargs)
            else:
                if request.method == 'POST':
                    output = self.action(*args, **kwargs, serializer=serializer)
                else:
                    output = self.action(*args, **kwargs)

            output = {
                'output': output,
                'time': round(time.time() - start_time, 2),
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }

            return await response_function(output, 200)
        except MlChainError as ex:
            err = ex.msg
            logger.error("code: {0} msg: {1}".format(ex.code, ex.msg))

            output = {
                'error': err,
                'time': round(time.time() - start_time, 2),
                'code': ex.code,
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
            return await response_function(output, ex.status_code)
        except AssertionError as ex:
            err = str(ex)
            logger.error(err)

            output = {
                'error': err,
                'time': round(time.time() - start_time, 2),
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
            return await response_function(output, 422)
        except Exception as ex:
            err = str(format_exc(name='mlchain.serve.server'))
            logger.error(err)

            output = {
                'error': err,
                'time': round(time.time() - start_time, 2),
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
            return await response_function(output, 500)


class QuartServer(MLServer):
    def __init__(self, model: ServeModel, name=None, version='0.0', trace=False, monitor_sampling_rate=0.0, dump_request=None,api_keys = None):
        MLServer.__init__(self, model, name)
        self.app = Quart(self.name,static_folder=STATIC_PATH, template_folder=TEMPLATE_PATH, static_url_path="/static")
        self.app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
        self.version = version
        self.dump_request = dump_request
        self.apm = apm.Client(config=apm_config, service_name=self.name) if trace else None
        self.converter = Converter(FileStorage,self._get_file_name,self._get_data)
        self.logger = None
        self.monitor_sampling_rate = monitor_sampling_rate
        self.api_keys = api_keys
        self.register_home()
        self._initalize_app()

    def register_home(self):
        @self.app.route("/", methods=['GET'])
        def home():
            return render_template("home.html", base_prefix=os.getenv('BASE_PREFIX', ''))

    def _get_file_name(self, storage):
        return storage.filename

    def _get_data(self, storage):
        return storage.read()

    def _add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET', 'POST']):
        """
        Add one endpoint to the flask application. Accept GET, POST and PUT.
        :param endpoint: Callable URL.
        :param endpoint_name: Name of the Endpoint
        :param handler: function to execute on call on the URL
        :return: Nothing
        """
        self.app.add_url_rule(endpoint, endpoint_name, QuartEndpointAction(handler, self.serializers_dict, self.dump_request,version=self.version,api_keys=self.api_keys),
                              methods=methods)

    async def __get_kwargs_from_request_FORM(self, args, kwargs, files_args, serializer):
        """
        Get all key, value of request.form
        """

        temp = await request.form
        result = defaultdict(list)
        for k, v in temp.items():
            result[k].append(v)
        temp = result

        for key, value in temp.items():
            if key == "MLCHAIN INPUT":
                data = serializer.decode(value[0].encode())
                args, kwargs = list(data['input'])
                files_args = data.get('files_args', {})
            elif len(value) == 1:
                kwargs[key] = value[0]
            else:
                kwargs[key] = value

        return args, kwargs, files_args

    async def __update_args_kwargs_from_request_FILES(self, args, kwargs, files_args):
        """
        Get all key, value of request.file
        """
        args = list(args)

        temp = await request.files
        result = defaultdict(list)
        for k, v in temp.items():
            result[k].append(v)
        temp = result

        for key, value in temp.items():
            if key in files_args:
                trace_position = files_args[key]
                if isinstance(trace_position, int):
                    args[files_args[key]] = value
                else:
                    args[trace_position[0]][trace_position[1]] = value
            else:
                if key in kwargs:
                    raise MLChainAssertionError("Only accept one param {0}".format(key))
                if len(value) == 1:
                    kwargs[key] = value[0]
                else:
                    kwargs[key] = value

        return tuple(args), kwargs

    async def __update_args_kwargs_from_request_ARGS(self, args, kwargs):
        """
        Get all key, value of request.args
        """
        temp = request.args
        result = defaultdict(list)
        for k, v in temp.items():
            result[k].append(v)
        temp = result

        for key, value in temp.items():
            if key in kwargs:
                raise MLChainAssertionError("Only accept one param {0}".format(key))
            if len(value) == 1:
                kwargs[key] = value[0]
            else:
                kwargs[key] = value

        return args, kwargs

    async def get_param_from_request(self, serializer):
        # Serializer POST data
        try:
            request_data = await request.data
            data = serializer.decode(request_data)
        except RequestEntityTooLarge:
            raise MlChainError('Request Entity Too Large: The data value transmitted exceeds the capacity limit!', status_code=413)
        except Exception as ex:
            request_data = str(request_data)
            if "Content-Type" in request_data:
                if re.search(r"input.*file_args", request_data) is not None:
                    logger.debug("ERROR: Can not decode request.data, serializer error: ", str(ex))
            elif "Content-Disposition" not in request_data:
                logger.debug("ERROR: Can not decode request.data, serializer error: ", str(ex))
            data = {}

        if "input" in data:
            args, kwargs = data['input']
            files_args = data.get('files_args', {})
        else:
            args, kwargs = (), {}
            files_args = {}

        args, kwargs, files_args = await self.__get_kwargs_from_request_FORM(args, kwargs, files_args, serializer)
        args, kwargs = await self.__update_args_kwargs_from_request_FILES(args, kwargs, files_args)
        args, kwargs = await self.__update_args_kwargs_from_request_ARGS(args, kwargs)
        return args, kwargs

    async def _call_function(self, function_name, serializer):
        if self.apm and 'Traceparent' in request.headers:
            trace_parent = apm.TraceParent.from_string(request.headers.get('Traceparent'))
        else:
            trace_parent = None
        log = (random.random() < self.monitor_sampling_rate or trace_parent is not None)
        id = None
        if self.apm and log:
            transaction = self.apm.begin_transaction(str(function_name), trace_parent=trace_parent)
            if transaction:
                id = transaction.id
        if function_name is None:
            raise AssertionError("You need to specify the function name (API name)")
        info = {}
        headers = {k:v for k,v in request.headers.items()}
        if isinstance(function_name, str):
            # Serializer POST data

            args, kwargs = await self.get_param_from_request(serializer)
            func = self.model.get_function(function_name)
            kwargs = self.get_kwargs(func, *args, **kwargs)
            kwargs = self._normalize_kwargs_to_valid_format(kwargs, func)
            if '__headers__' in kwargs:
                headers = kwargs.pop('__headers__')
            try:
                start = time.time()
                output = await self.model.call_async_function(function_name, None,__headers__ = headers, **kwargs)
                duration = time.time() - start
                info["time"] = duration
                # Response data
                if self.apm and log:
                    self.apm.end_transaction(str(function_name), result="done")

                if self.logger and log:
                    self.logger.log(info, id=id, function_name=function_name, **kwargs)
            except Exception as e:
                if self.apm and log:
                    self.apm.capture_exception()
                    self.apm.end_transaction(self.name, result="error")
                info['error'] = True
                info['time'] = 0
                if self.logger and log:
                    self.logger.log(info, id=id, function_name=function_name, **kwargs)
                raise e
        else:
            if self.apm and log:
                self.apm.end_transaction(self.name, result="error")
            info['error'] = True
            info['time'] = 0
            if self.logger and log:
                self.logger.log(info, id=id, function_name=str(function_name))
            raise AssertionError("function_name must be str")
        return output

    def register_swagger(self, host, port):
        swagger_ui = Blueprint("swagger",
                               __name__,
                               static_folder=os.path.join(TEMPLATE_PATH,'swaggerui'))

        swagger_template = SwaggerTemplate(os.getenv("BASE_PREFIX", '/'), [{'name': self.name}], title=self.name,
                                           description=self.model.model.__doc__, version=self.model.name)
        for name, func in self.model.get_all_func().items():
            swagger_template.add_endpoint(func, f'/call/{name}', tags=[self.name])

        SWAGGER_URL = '/swagger'
        API_URL = '/swagger_json'

        @swagger_ui.route('{0}/'.format(SWAGGER_URL))
        @swagger_ui.route('{0}/<path:path>'.format(SWAGGER_URL))
        def show(path=None):
            if path is None:
                return send_from_directory(
                    swagger_ui._static_folder,
                    "index.html"
                )
            if path == 'swagger.json':
                return jsonify(swagger_template.template)
            if isinstance(path,str):
                path = path.strip('.')
            return send_from_directory(
                swagger_ui._static_folder,
                path
            )

        self.app.register_blueprint(swagger_ui)

    def run(self, host='127.0.0.1', port=8080, bind=None,
            cors=False, cors_allow_origins="*", gunicorn=False, hypercorn=True, debug=False, use_reloader=False,
            workers=1, timeout=60,
            keepalive=5, max_requests=0, threads=1, worker_class='asyncio', umask='0', **kwargs):
        """
        Run a server from a Python class
        :model: Your model class
        :host: IP address you want to start server
        :port: Port to start server at
        :bind: Gunicorn: The socket to bind. A list of string or string of the form: HOST, HOST:PORT, unix:PATH, fd://FD. An IP is a valid HOST.
        :deny_all_function: Default is False, which enable all function except function with @except_serving or function in blacklist, True is deny all and you could use with whitelist
        :blacklist: All listing function name here won't be served
        :whitelist: Served all function name inside whitelist
        :cors: Enable CORS or not
        :cors_resources: Config Resources of flask-cors
        :cors_allow_origins: Allow host of cors
        :gunicorn: Run with Gunicorn or not
        :debug: Debug or not
        :use_reloader: Default False, which is using 1 worker in debug instead of 2
        :timeout: Timeout of each request
        :keepalive: The number of seconds to wait for requests on a Keep-Alive connection.
        :threads: The number of worker threads for handling requests. Be careful, threads would break your result if it is bigger than 1
        :worker_class: The type of workers to use.
        :max_requests: Max Request to restart Gunicorn Server, default is 0 which means no restart
        :umask: A bit mask for the file mode on files written by Gunicorn.
        :kwargs: Other Gunicorn options
        """
        if not ((sys.version_info.major == 3 and sys.version_info.minor >= 6) or sys.version_info.major > 3):
            raise Exception("Quart must be use with Python 3.7 or higher")

        if not isinstance(bind, list) and not isinstance(bind, str) and bind is not None:
            raise AssertionError(
                "Bind have to be list or string of the form: HOST, HOST:PORT, unix:PATH, fd://FD. An IP is a valid HOST.")

        if cors:
            CORS(self.app, allow_origin=cors_allow_origins)
        try:
            self.register_swagger(host, port)
        except Exception as e:
            logger.error("Can't register swagger with error {0}".format(e))

        if not gunicorn and not hypercorn:
            if bind is not None:
                logger.warning("Quart only use host and port to run, not bind")

            logger.info("-" * 80)
            logger.info("Served model with Quart at host={0}, port={1}".format(host, port))
            logger.info("Debug = {}".format(debug))
            logger.info("-" * 80)

            self.app.run(host=host, port=port, debug=debug, use_reloader=use_reloader)
        elif hypercorn:
            # Process bind, host, port
            if isinstance(bind, str):
                bind = [bind]

            bind_host_port = '%s:%s' % (host, port)
            if not bind:
                bind = [bind_host_port]

            logger.info("-" * 80)
            logger.info("Served model with Quart and Hypercorn at bind={}".format(bind))
            logger.warning("timeout, threads, max_requests is not work here")
            if 'uvloop' not in worker_class:
                logger.info("You could use worker_class=uvloop for better performance. It isn't work on Windows")
            logger.info("Number of workers: {}".format(workers))
            logger.info("Debug = {}".format(debug))
            logger.info("-" * 80)

            loglevel = kwargs.get('loglevel', 'warning' if debug else 'info')
            gunicorn_server = HypercornWrapper(self.app, bind=bind, workers=workers,
                                               keep_alive_timeout=keepalive, loglevel=loglevel,
                                               worker_class=worker_class, umask=int(umask), **kwargs).run()
        else:
            # Process bind, host, port
            if isinstance(bind, str):
                bind = [bind]

            bind_host_port = '%s:%s' % (host, port)
            if bind is None:
                bind = [bind_host_port]

            worker_class = 'uvicorn.workers.UvicornWorker'

            logger.info("-" * 80)
            logger.info("Served model with Quart and Gunicorn at bind={}".format(bind))
            logger.info("Number of workers: {}".format(workers))
            logger.info("Number of threads: {}".format(threads))
            logger.info("API timeout: {}".format(timeout))
            logger.info("Debug = {}".format(debug))
            logger.info("-" * 80)

            loglevel = kwargs.get('loglevel', 'warning' if debug else 'info')
            gunicorn_server = GunicornWrapper(self.app, bind=bind, workers=workers, timeout=timeout,
                                              keepalive=keepalive, max_requests=max_requests, loglevel=loglevel,
                                              threads=threads, worker_class=worker_class, umask=umask, **kwargs).run()
