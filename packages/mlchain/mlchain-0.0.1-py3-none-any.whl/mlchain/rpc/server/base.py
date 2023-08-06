from mlchain.base import ServeModel
from mlchain.base.serializer import JsonSerializer, MsgpackSerializer, MsgpackBloscSerializer
import warnings
from typing import *
from mlchain.base.converter import Converter
from inspect import signature
from inspect import _empty
from collections import defaultdict
from fuzzywuzzy.fuzz import ratio


class MLServer:
    convert_dict = defaultdict(dict)
    file_converters = {}
    def __init__(self, model: ServeModel, name=None):
        if not isinstance(model, ServeModel):
            model = ServeModel(model)
        self.model = model
        self.name = name or model.name
        self.serializers_dict = {
            'application/json': JsonSerializer(),
            'application/msgpack': MsgpackSerializer(),
        }
        try:
            self.serializers_dict['application/msgpack_blosc'] = MsgpackBloscSerializer()
        except:
            self.serializers_dict['application/msgpack_blosc'] = self.serializers_dict['application/msgpack']
            warnings.warn("Can't load MsgpackBloscSerializer. Use msgpack instead")
        self.converter = Converter()

    # @staticmethod
    # def add_convert(function):
    #     sig = signature(function)
    #     parameters = sig.parameters
    #     for key, input_types in parameters.items():
    #         input_types = input_types.annotation
    #         output_types = sig.return_annotation
    #         if input_types == Union:
    #             input_types = input_types.__args__
    #         else:
    #             input_types = [input_types]
    #
    #         if output_types == Union:
    #             output_types = output_types.__args__
    #         else:
    #             output_types = [output_types]
    #
    #         for i_type in input_types:
    #             for o_type in output_types:
    #                 MLServer.convert_dict[i_type][o_type] = function
    #         break
    #
    # @staticmethod
    # def add_convert_file(extensions, function, output_type = None):
    #     sig = signature(function)
    #     input_types = extensions.split(',')
    #     input_types = tuple(sorted(e.strip() for e in input_types))
    #     if output_type is None:
    #         output_types = sig.return_annotation
    #
    #         if output_types == Union:
    #             output_types = output_types.__args__
    #         else:
    #             output_types = (output_types,)
    #     else:
    #         output_types = (output_type,)
    #     for o_type in output_types:
    #         MLServer.file_converters[(input_types,o_type)]= function

    def _check_status(self):
        """
        Check status of a served model
        """
        return "pong"

    def _add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET', 'POST']):
        """
        Add one endpoint to the flask application. Accept GET, POST and PUT.
        :param endpoint: Callable URL.
        :param endpoint_name: Name of the Endpoint
        :param handler: function to execute on call on the URL
        :return: Nothing
        """
        raise NotImplementedError

    def _initalize_app(self):
        """
        Initalize all endpoint of server
        """

        self._add_endpoint('/api/get_params_<function_name>', '_get_parameters_of_func',
                           handler=self.model._get_parameters_of_func, methods=['GET'])
        self._add_endpoint('/api/des_func_<function_name>', '_get_description_of_func',
                           handler=self.model._get_description_of_func, methods=['GET'])

        self._add_endpoint('/api/ping', '_check_status', handler=self._check_status, methods=['GET'])
        self._add_endpoint('/api/description', '_get_all_description', handler=self.model._get_all_description,
                           methods=['GET'])
        self._add_endpoint('/api/list_all_function', '_list_all_function', handler=self.model._list_all_function,
                           methods=['GET'])
        self._add_endpoint('/api/list_all_function_and_description', '_list_all_function_and_description',
                           handler=self.model._list_all_function_and_description, methods=['GET'])

        # Each valid serve function of model will be an endpoint of server
        self._add_endpoint('/call/<function_name>', '__call_function', handler=self._call_function, methods=['POST'])
        # self._add_endpoint('/result/<key>', '__result', handler=self.model.result, methods=['GET'])
    # def convert_file(self,file_name,data,out_type):
    #     ext = file_name.rsplit('.')[-1].lower()
    #     out_type = Union[out_type]
    #     if out_type == Union:
    #         out_type = out_type.__args__
    #     else:
    #         out_type = (out_type,)
    #     for (k,o),converter in self.file_converters.items():
    #         if (ext in k or '*' in k) and (out_type == o or o in out_type):
    #             return converter(file_name,data)
    #     raise MLChainAssertionError("Not found convert file {0} to {1}".format(file_name,out_type))

    def convert(self, value, out_type):
        return self.converter.convert(value,out_type)

        # if out_type == _empty:
        #     return value
        # if getattr(out_type,'__origin__',None) in [List,Set,Dict,list,set,dict] and out_type.__origin__ is not None:
        #     if isinstance(value,(List,list)):
        #         if out_type.__origin__ in [List,list]:
        #             return [self.convert(v,out_type.__args__) for v in value]
        #         elif out_type.__origin__ in [Set,set]:
        #             return set(self.convert(v,out_type.__args__) for v in value)
        #     elif isinstance(value,(Dict,dict)):
        #         if out_type.__origin__ in [Dict,list]:
        #             args = out_type.__args__
        #             if len(args)==2:
        #                 return {self.convert(k,args[0]):self.convert(v,args[1]) for k,v in value.items()}
        #             elif len(args) == 1:
        #                 return {k: self.convert(v, args[0]) for k, v in value.items()}
        #     else:
        #         if type(value) == self.FILE_STORAGE_TYPE:
        #             return self.convert_file(self._get_file_name(value), self._get_data(value), out_type)
        #         if out_type.__origin__ in [List,list]:
        #             return [self.convert(value,out_type.__args__)]
        #         elif out_type.__origin__ in [Set,set]:
        #             return {self.convert(value,out_type.__args__)}
        #         else:
        #             raise MLChainAssertionError("Can't convert value {0} to {1}".format(value,out_type),code="convert")
        # else:
        #     try:
        #         if isinstance(value, out_type):
        #             return value
        #     except:
        #         pass
        # out_type = Union[out_type]
        # if out_type == Union:
        #     out_type = out_type.__args__
        # else:
        #     out_type = (out_type,)
        # if type(value) in out_type:
        #     return value
        # else:
        #     for i_type in self.convert_dict:
        #         if isinstance(value, i_type):
        #             for o_type in self.convert_dict[i_type]:
        #                 if o_type in out_type:
        #                     return self.convert_dict[i_type][o_type](value)
        # if type(value) == self.FILE_STORAGE_TYPE:
        #     return self.convert_file(self._get_file_name(value),self._get_data(value),out_type)
        # raise MLChainAssertionError("Not found converter from {0} to {1}".format(type(value),out_type))
        # return value

    def _normalize_kwargs_to_valid_format(self, kwargs, func_):
        """
        Normalize data into right formats of func_
        """
        inspect_func_ = signature(func_)

        accept_kwargs = "**" in str(inspect_func_)

        # Check valid parameters
        for key, value in list(kwargs.items()):
            if key in inspect_func_.parameters:
                req_type = inspect_func_.parameters[key].annotation
                kwargs[key] = self.convert(value, req_type)
            elif not accept_kwargs:
                suggest = None
                fuzz = 0
                for k in inspect_func_.parameters:
                    if suggest is None:
                        suggest = k
                        fuzz = ratio(k.lower(),key.lower())
                    elif ratio(k.lower(),key.lower()) > fuzz:
                        suggest = k
                        fuzz = ratio(k.lower(), key.lower())
                if suggest is not None:
                    suggest = ", did you mean: {0}".format(suggest)
                else:
                    suggest = '.'
                kwargs.pop(key)
                available_params = [k for k in inspect_func_.parameters]
                # raise AssertionError("Not found param {0}{1}. Available params {2}".format(key,suggest,available_params
                #                                                                            ))

        missing = []
        for key,parameter in inspect_func_.parameters.items():
            if key not in kwargs and parameter.default == _empty:
                missing.append(key)
        if len(missing)>0:
            raise AssertionError("Missing params {0}".format(missing))
        return kwargs

    def get_kwargs(self, func, *args, **kwargs):
        sig = signature(func)
        parameters = sig.parameters

        kwgs = {}
        for key, value in zip(parameters.keys(), args):
            kwgs[key] = value
        kwgs.update(kwargs)
        return kwgs

    def _call_function(self, *args, **kwargs):
        """
        Flow request values into function_name and return output
        """
        raise NotImplementedError

# MLServer.add_convert(str2ndarray)
# MLServer.add_convert(list2ndarray)
# MLServer.add_convert(str2int)
# MLServer.add_convert(str2float)
# MLServer.add_convert(str2bool)
# MLServer.add_convert(str2bytes)
# MLServer.add_convert(str2list)
# MLServer.add_convert(str2dict)
# MLServer.add_convert_file('jpg,jpeg,png,gif,bmp,jpe,jp2,pbm,pgm,ppm,sr,ras',cv2imread,output_type=np.ndarray)
# MLServer.add_convert_file('jpg,jpeg,png,gif,bmp,jpe,jp2,pbm,pgm,ppm,sr,ras',cv2imread_to_list,output_type=List[np.ndarray])
# MLServer.add_convert_file('tif,tiff',pilimread_one_img,output_type=np.ndarray)
# MLServer.add_convert_file('tif,tiff', pilimread_list_img, output_type=List[np.ndarray])
# MLServer.add_convert_file('*', storage2bytes, output_type=bytes)
# MLServer.add_convert_file('json', storage2json, output_type=dict)
# MLServer.add_convert_file('txt', storage2str, output_type=str)

