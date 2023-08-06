from .base import MLClient,BaseFunction
import httpx
from mlchain.storage import Path
from mlchain.base.log import except_handler
import uuid
import os


class HttpModel(MLClient):
    def __init__(self, api_key=None, api_address=None, serializer='msgpack', image_encoder=None, name=None,
                 version='lastest', check_status=False, headers = None, **kwargs):
        MLClient.__init__(self, api_key=api_key, api_address=api_address, serializer=serializer,
                          image_encoder=image_encoder, name=name,
                          version=version, check_status=check_status, headers= headers, **kwargs)
        if isinstance(self.api_address, str):
            self.api_address = self.api_address.strip()
            if len(self.api_address) > 0 and self.api_address[-1] == '/':
                self.api_address = self.api_address[:-1]

            if len(self.api_address) > 0 and self.api_address[0] != 'h':
                self.api_address = 'http://{0}'.format(api_address)

        self.content_type = 'application/{0}'.format(self.serializer_type)
        if check_status:
            output_description = self.get('description')
            if 'error' in output_description:
                with except_handler():
                    raise AssertionError("ERROR: Model {0} in version {1} is not found".format(name, version))
            else:
                output_description = output_description['output']
                self.__doc__ = output_description['__main__']
                self.all_func_des = output_description['all_func_des']
                self.all_func_params = output_description['all_func_params']
                self.all_attributes = output_description['all_attributes']

    def __format_error(self, response):
        if response.status_code == 404:
            return {
                'error': 'This request url is not found',
                'time': 0
            }
        else:
            try:
                error = self.serializer.decode(response.content)
            except:
                error = self.json_serializer.decode(response.content)

            if 'error' in error:
                return error
            else:
                return {
                    'error': 'Server run error, please try again',
                    'time': 0
                }

    def check_response_ok(self, response):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        try:
            response.raise_for_status()
        except:
            return False
        return True

    def _get(self, api_name, headers=None):
        """
        GET data from url
        """
        if headers is None:
            headers = {}
        headers = {
            'Content-type': self.content_type,
            **headers
        }
        if self.api_key is not None:
            headers['x-api-key'] = self.api_key

        with httpx.Client(timeout=self.timeout) as client:
            output = client.get("{0}/api/{1}".format(self.api_address, api_name), headers=headers)

        if not self.check_response_ok(output):
            return self.__format_error(output)

        output_decoded = self.serializer.decode(output.content)
        return output_decoded

    def _post(self, function_name, headers=None, args=None, kwargs=None):
        files_args = {}
        files = []
        # Process files in args
        for idx, item in enumerate(args):
            if isinstance(item, Path):
                new_file_name = str(uuid.uuid4())

                args[idx] = ""
                files.append((new_file_name, (os.path.split(item)[1], open(item, 'rb'), 'application/octet-stream')))
                files_args[new_file_name] = idx
            elif isinstance(item, list) and all([isinstance(x, Path) for x in item]):
                for sub_idx, sub_item in enumerate(item):
                    new_file_name = str(uuid.uuid4())
                    item[sub_idx] = ""

                    files.append(
                        (new_file_name, (os.path.split(sub_item)[1], open(sub_item, 'rb'), 'application/octet-stream')))
                    files_args[new_file_name] = (idx, sub_idx)

        # Process files in kwargs
        drop_key = []
        for key, item in kwargs.items():
            if isinstance(item, Path):
                kwargs[key] = ""
                files.append((key, (os.path.split(item)[1], open(item, 'rb'), 'application/octet-stream')))
                drop_key.append(key)
            elif isinstance(item, list) and all([isinstance(x, Path) for x in item]):
                for sub_idx, sub_item in enumerate(item):
                    item[sub_idx] = ""

                    files.append((key, (os.path.split(sub_item)[1], open(sub_item, 'rb'), 'application/octet-stream')))
                drop_key.append(key)

        for key in drop_key:
            kwargs.pop(key)

        input = {
            'input': (tuple(args), kwargs),
            'files_args': files_args
        }

        if headers is None:
            headers = {}
        headers = {
            'Content-type': self.content_type,
            **headers
        }
        if self.api_key is not None:
            headers['x-api-key'] = self.api_key

        with httpx.Client(timeout=self.timeout) as client:
            if len(files) > 0:
                # It must be Json here
                input_encoded = self.json_serializer.encode(input)

                files.append(("MLCHAIN INPUT", (None, input_encoded, 'application/octet-stream')))
                headers.pop("Content-type")
                headers['serializer'] = "application/json"  # Msgpack hasn't supported yet

                output = client.post("{0}/call/{1}".format(self.api_address, function_name), headers=headers,
                                     files=files)
            else:
                input_encoded = self.serializer.encode(input)
                output = client.post("{0}/call/{1}".format(self.api_address, function_name), data=input_encoded,
                                     headers=headers)

        if not self.check_response_ok(output):
            return self.__format_error(output)

        return output.content
