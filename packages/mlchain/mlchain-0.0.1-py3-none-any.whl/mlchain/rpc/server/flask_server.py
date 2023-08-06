from mlchain.base.serve_model import ServeModel
from mlchain.base.wrapper import GunicornWrapper
from mlchain.base.log import logger, format_exc
from mlchain.base.exceptions import MlChainError, MLChainAssertionError
from flask import Flask, request, jsonify, Response, send_file, render_template, Blueprint, send_from_directory
from flask_cors import CORS
from .swagger import SwaggerTemplate
from .autofrontend import AutofrontendConfig
from .base import MLServer, Converter
from mlchain.observe import apm
from typing import *
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge
from mlchain.config import apm_config
import time
import random
import json
import os
import re
import mlchain
from uuid import uuid4
from io import BytesIO
from werkzeug.http import parse_options_header

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'server/templates')
STATIC_PATH = os.path.join(APP_PATH, 'server/static')


class FlaskEndpointAction(object):
    """
    Defines an Flask Endpoint for a specific action for any client.
    """

    def __init__(self, action, serializers_dict, dump_request=None, version='latest', api_keys=None):
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

    def __get_json_response(self, output, status=200, metadata=None):
        """
        Get JSON Reponse
        """
        output_encoded = self.json_serializer.encode(output)
        if isinstance(self.dump_request, str) and isinstance(metadata, dict) and 'id' in metadata:
            open(os.path.join(self.dump_request, 'output', metadata['id']), 'wb').write(output_encoded)
            json.dump(metadata,
                      open(os.path.join(self.dump_request, 'metadata', metadata['id']), 'w', encoding='utf-8'),
                      ensure_ascii=False)
        return Response(output_encoded, mimetype='application/json', status=status)

    def __get_msgpack_response(self, output, status=200, metadata=None):
        """
        Get msgpack Reponse
        """
        output_encoded = self.msgpack_serializer.encode(output)
        if isinstance(self.dump_request, str) and isinstance(metadata, dict) and 'id' in metadata:
            open(os.path.join(self.dump_request, 'output', metadata['id']), 'wb').write(output_encoded)
            json.dump(metadata,
                      open(os.path.join(self.dump_request, 'metadata', metadata['id']), 'w', encoding='utf-8'),
                      ensure_ascii=False)
        return Response(output_encoded, mimetype='application/msgpack', status=status)

    def __get_msgpack_blosc_response(self, output, status=200, metadata=None):
        """
        Get msgpack blosc response
        """
        output_encoded = self.msgpack_blosc_serializer.encode(output)
        if isinstance(self.dump_request, str) and isinstance(metadata, dict) and 'id' in metadata:
            open(os.path.join(self.dump_request, 'output', metadata['id']), 'wb').write(output_encoded)
            json.dump(metadata,
                      open(os.path.join(self.dump_request, 'metadata', metadata['id']), 'w', encoding='utf-8'),
                      ensure_ascii=False)
        return Response(output_encoded, mimetype='application/msgpack_blosc', status=status)

    def __call__(self, *args, **kwargs):
        """
        Standard method that effectively perform the stored action of this endpoint.
        :param args: Arguments to give to the stored function
        :param kwargs: Keywords Arguments to give to the stored function
        :return: The response, which is a jsonified version of the function returned value
        """
        start_time = time.time()

        # If data POST is in msgpack format
        serializer = self.serializers_dict.get(request.content_type, self.serializers_dict[
            request.headers.get('serializer', 'application/json')])
        if request.content_type == 'application/msgpack':
            response_function = self.__get_msgpack_response
        elif request.content_type == 'application/msgpack_blosc':
            response_function = self.__get_msgpack_blosc_response
        else:
            response_function = self.__get_json_response
        metadata = {}
        if request.method == 'POST' and self.api_keys is not None or (
                isinstance(self.api_keys, (list, dict)) and len(self.api_keys) > 0):
            authorized = False
            has_key = False
            for key in ['x-api-key', 'apikey', 'apiKey', 'api-key']:
                apikey = request.headers.get(key, '')
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
                    'error': error,
                    'api_version': self.version,
                    'mlchain_version': mlchain.__version__
                }
                return response_function(output, 401, metadata)
        try:
            # Perform the action
            if request.method == 'POST':
                output = self.action(*args, **kwargs, serializer=serializer, metadata=metadata)
            else:
                output = self.action(*args, **kwargs)
            output = {
                'output': output,
                'time': round(time.time() - start_time, 2),
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
            metadata['status_code'] = 200
            return response_function(output, 200, metadata)
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
            metadata['status_code'] = ex.status_code
            return response_function(output, ex.status_code)
        except AssertionError as ex:
            err = str(ex)
            logger.error(err)

            output = {
                'error': err,
                'time': round(time.time() - start_time, 2),
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
            metadata['status_code'] = 422
            return response_function(output, 422)
        except Exception as ex:
            err = str(format_exc(name='mlchain.serve.server'))
            logger.error(err)

            output = {
                'error': err,
                'time': round(time.time() - start_time, 2),
                'api_version': self.version,
                'mlchain_version': mlchain.__version__
            }
            metadata['status_code'] = 500
            return response_function(output, 500)


class FlaskServer(MLServer):
    def __init__(self, model: ServeModel, name=None, version='0.0', trace=False, log=False,
                 monitor_sampling_rate=0.0, dump_request=None, api_keys=None):
        MLServer.__init__(self, model, name)
        self.app = Flask(self.name, static_folder=STATIC_PATH, template_folder=TEMPLATE_PATH, static_url_path="/static")
        self.app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
        self.version = version
        self.apm = apm.Client(config=apm_config, service_name=self.name) if trace else None
        self.converter = Converter(FileStorage, self._get_file_name, self._get_data)
        self.logger = None
        self.model.log = min(monitor_sampling_rate, log)
        self.monitor_sampling_rate = monitor_sampling_rate
        self.register_home()
        self.dump_request = dump_request
        self.api_keys = api_keys
        if isinstance(dump_request, str):
            os.makedirs(os.path.join(dump_request, 'metadata'), exist_ok=True)
            os.makedirs(os.path.join(dump_request, 'input'), exist_ok=True)
            os.makedirs(os.path.join(dump_request, 'output'), exist_ok=True)
        self._initalize_app()

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
        self.app.add_url_rule(endpoint, endpoint_name,
                              FlaskEndpointAction(handler, self.serializers_dict, self.dump_request,
                                                  version=self.version, api_keys=self.api_keys),
                              methods=methods)

    def __get_kwargs_from_request_FORM(self, args, kwargs, files_args, serializer):
        """
        Get all key, value of request.form
        """
        try:
            temp = request.form.to_dict(flat=False)
        except RequestEntityTooLarge:
            raise MlChainError('Request Entity Too Large: The data value transmitted exceeds the capacity limit!',
                               status_code=413)

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

    def __update_args_kwargs_from_request_FILES(self, args, kwargs, files_args):
        """
        Get all key, value of request.file
        """
        args = list(args)

        temp = request.files.to_dict(flat=False)

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

    def __update_args_kwargs_from_request_ARGS(self, args, kwargs):
        """
        Get all key, value of request.args
        """
        temp = request.args.to_dict(flat=False)

        for key, value in temp.items():
            if key in kwargs:
                raise MLChainAssertionError("Only accept one param {0}".format(key))
            if len(value) == 1:
                kwargs[key] = value[0]
            else:
                kwargs[key] = value

        return args, kwargs

    def get_param_from_request(self, serializer):
        try:
            data = serializer.decode(request.data)
        except Exception as ex:
            logger.debug(format_exc(name='mlchain.serve.flask_server decode data'))
            logger.debug("ERROR: Can not decode request.data")
            data = {}

        if "input" in data:
            args, kwargs = data['input']
            files_args = data.get('files_args', {})
        else:
            args, kwargs = (), {}
            files_args = {}

        args, kwargs, files_args = self.__get_kwargs_from_request_FORM(args, kwargs, files_args, serializer)
        args, kwargs = self.__update_args_kwargs_from_request_FILES(args, kwargs, files_args)
        args, kwargs = self.__update_args_kwargs_from_request_ARGS(args, kwargs)
        return args, kwargs

    def _call_function(self, function_name, serializer, metadata):
        if self.apm and 'Traceparent' in request.headers:
            trace_parent = apm.TraceParent.from_string(request.headers.get('Traceparent'))
        else:
            trace_parent = None
        log = (random.random() < self.monitor_sampling_rate or trace_parent is not None)
        id = uuid4().hex
        if self.apm and log:
            transaction = self.apm.begin_transaction(str(function_name), trace_parent=trace_parent)
            if transaction:
                id = transaction.id
        if function_name is None:
            raise AssertionError("You need to specify the function name (API name)")
        info = {}
        received_time = time.time()
        logger.info("function: {0}\tid: {1}".format(function_name, id))
        headers = {key: value for (key, value) in request.headers}
        if isinstance(self.dump_request, str):
            metadata['headers'] = headers
            metadata['path'] = request.path
            metadata['method'] = request.method
            metadata['cookies'] = request.cookies
            metadata['host_url'] = request.host_url
            metadata['received_time'] = received_time
            metadata['id'] = id
            data = request.stream.read()
            open(os.path.join(self.dump_request, 'input', id), 'wb').write(data)
            json.dump(metadata,
                      open(os.path.join(self.dump_request, 'metadata', id), 'w', encoding='utf-8'),
                      ensure_ascii=False)
            content_type = request.content_type
            content_length = request.content_length
            mimetype, options = parse_options_header(content_type)
            parser = request.make_form_data_parser()
            data = parser.parse(
                BytesIO(data), mimetype, content_length, options
            )
            d = request.__dict__
            d["stream"], d["form"], d["files"] = data

        if isinstance(function_name, str):
            # Serializer POST data
            args, kwargs = self.get_param_from_request(serializer)
            func = self.model.get_function(function_name)
            kwargs = self.get_kwargs(func, *args, **kwargs)
            kwargs = self._normalize_kwargs_to_valid_format(kwargs, func)
            if '__headers__' in kwargs:
                headers = kwargs.pop('__headers__')
            try:
                start = time.time()
                output = self.model.call_function(function_name, id, __headers__=headers, **kwargs)
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
                               static_folder=os.path.join(TEMPLATE_PATH, 'swaggerui'))

        swagger_template = SwaggerTemplate(os.getenv("BASE_PREFIX", '/'), [{'name': self.name}], title=self.name,
                                           description=self.model.model.__doc__, version=self.model.name)
        for name, func in self.model.get_all_func().items():
            swagger_template.add_endpoint(func, f'/call/{name}', tags=[self.name])

        SWAGGER_URL = '/swagger'

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
            if isinstance(path, str):
                path = path.strip('.')
            return send_from_directory(
                swagger_ui._static_folder,
                path
            )

        self.app.register_blueprint(swagger_ui)

    def register_autofrontend(self, host, port, endpoint=None, mlchain_management=None):
        if endpoint is None:
            endpoint = ''
        autofrontend_template = AutofrontendConfig(endpoint, title=self.name)
        if self.model.config is not None:
            out_configs = self.model.config
        else:
            out_configs = {}
        for name, func in self.model.get_all_func().items():
            if name in out_configs:
                out_config = out_configs[name]
                if 'config' in out_config:
                    config = out_config['config']
                else:
                    config = None
                if 'example' in out_config:
                    @self.app.route(f'/sample/{name}', methods=['POST', 'GET'])
                    def sample():
                        return jsonify({'output': out_config['example']})

                    sample_url = f'{endpoint}/sample/{name}'
                else:
                    sample_url = None
            else:
                config = None
                sample_url = None
            autofrontend_template.add_endpoint(func, f'{endpoint}/call/{name}', output_config=config,
                                               sample_url=sample_url)
        if os.path.exists("Readme.md"):
            description = open("Readme.md", encoding='utf-8').read()
        else:
            description = ""

        if os.path.exists("changelog.md"):
            changelog = open("changelog.md", encoding='utf-8').read()
        else:
            changelog = ""

        @self.app.route('/model', methods=['GET', 'POST'])
        def model_summary():
            return jsonify(autofrontend_template.summary)

        @self.app.route('/model/demo', methods=['GET', 'POST'])
        def demo_config():
            return jsonify(autofrontend_template.config)

        @self.app.route('/model/description', methods=['GET', 'POST'])
        def model_description():
            return Response(json.dumps({"value": description}), status=404)

        @self.app.route('/model/changelog', methods=['GET', 'POST'])
        def model_changelog():
            return Response(json.dumps({"value": changelog}), status=404)

        if mlchain_management and mlchain.model_id is not None:
            config_version = {
                "model_id": mlchain.model_id,
                "version": self.version,
                "input_config": autofrontend_template.input_config,
                "output_config": autofrontend_template.output_config,
                'endpoint': endpoint,
                'readme': description,
                'changelog': changelog
            }
            try:
                import requests
                r = requests.post(mlchain_management, json=config_version)
            except:
                pass

    def register_home(self):
        @self.app.route("/", methods=['GET'])
        def home():
            return render_template("home.html", base_prefix=os.getenv('BASE_PREFIX', ''))

    def run(self, host='127.0.0.1', port=8080, bind=None, cors=False, cors_resources={}, cors_allow_origins='*',
            gunicorn=False, debug=False, use_reloader=False,
            workers=1, timeout=60, keepalive=10, max_requests=0, threads=1, worker_class='gthread', umask='0',
            endpoint=None, mlchain_management=None,
            **kwargs):
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
        :workers: Number of workers to run Gunicorn
        :timeout: Timeout of each request
        :keepalive: The number of seconds to wait for requests on a Keep-Alive connection.
        :threads: The number of worker threads for handling requests. Be careful, threads would break your result if it is bigger than 1
        :worker_class: The type of workers to use.
        :max_requests: Max Request to restart Gunicorn Server, default is 0 which means no restart
        :umask: A bit mask for the file mode on files written by Gunicorn.
        :kwargs: Other Gunicorn options
        """
        if cors:
            CORS(self.app, resources=cors_resources, origins=cors_allow_origins)
        try:
            self.register_swagger(host, port)
        except Exception as e:
            logger.error("Can't register swagger with error {0}".format(e))

        try:
            self.register_autofrontend(host, port, endpoint=endpoint, mlchain_management=mlchain_management)
        except Exception as e:
            logger.error("Can't register autofrontend with error {0}".format(e))
        if not gunicorn:
            if bind is not None:
                if isinstance(bind, str):
                    bind = [bind]
                if isinstance(bind, list):
                    for ip_port in bind:
                        if re.match(r'(localhost:|((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|:)){4})\d+', ip_port):
                            logger.warning("Using host and port in bind to runserver")
                            host, port = ip_port.split(":")

            logger.info("-" * 80)
            logger.info("Served model with Flask at host={0}, port={1}".format(host, port))
            logger.info("Debug = {}".format(debug))
            logger.info("-" * 80)

            self.app.run(host=host, port=port, debug=debug, use_reloader=use_reloader, threaded=threads > 1)
        else:
            # Process bind, host, port
            if isinstance(bind, str):
                bind = [bind]

            bind_host_port = '%s:%s' % (host, port)
            if bind is None:
                bind = [bind_host_port]

            logger.info("-" * 80)
            logger.info("Served model with Flask and Gunicorn at bind={}".format(bind))
            logger.info("Number of workers: {}".format(workers))
            logger.info("Number of threads: {}".format(threads))
            logger.info("API timeout: {}".format(timeout))
            logger.info("Debug = {}".format(debug))
            logger.info("-" * 80)

            loglevel = kwargs.get('loglevel', 'warning' if debug else 'info')
            gunicorn_server = GunicornWrapper(self.app, bind=bind, workers=workers, timeout=timeout,
                                              keepalive=keepalive, max_requests=max_requests, loglevel=loglevel,
                                              worker_class=worker_class, threads=threads, umask=umask, **kwargs).run()
