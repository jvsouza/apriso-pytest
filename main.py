
import configparser
import json
import logging
import requests
from urllib.parse import urlunsplit
from zeep import Client

class UnitTest:
    def __init__(self, _file_config):
        _config = self.get_config_ini(_file_config)
        self.protocol = _config['basic']['protocol']
        self.ws_path_rest = _config['basic']['ws_path_rest']
        self.ws_path_soap = _config['basic']['ws_path_soap']
        self.host = _config['server']['host']
        self.ws_type = _config['webservice']['ws_type']
        self.ws_name = _config['webservice']['ws_name']
        self.debug = _config['basic']['debug'].lower() == "true"

        if self.debug:

            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            
            # handler external file
            file_handler = logging.FileHandler("logger.log")
            file_formatter = logging.Formatter('%(asctime)s > %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # handler print screen
            stream_handler = logging.StreamHandler()
            stream_formatter = logging.Formatter('%(asctime)s > %(message)s')
            stream_handler.setFormatter(stream_formatter)
            self.logger.addHandler(stream_handler)

            for section in _config.sections():
                self.logger.debug(f"[{section}]")
                for option in _config.options(section):
                    value = _config.get(section, option)
                    self.logger.debug(f"{option} = {value}")

    def get_config_ini(self, _file_name):
        '''
            purpose: get the parameterization made in the file referenced in the _file_name argument
            arguments:
                self : [UnitTest] (object instance)
                _file_name : [str] (complete address of the parameterization file)
            return: [ConfigParser] (object with the values of the parameterizations)
        '''
        config = configparser.ConfigParser()
        config.read(_file_name)
        return config

    def get_input_default(self, _operation, _inputs ):
        '''
            purpose: get the standard input structure
            arguments:
                self : [UnitTest] (object instance)
                _operation : [str] (name of the operation to test)
                _inputs : [dict] (input setup to test operation)
            return: [dict] (specific populated standard input: REST or SOAP)
        '''
        # the default SOAP input in Apriso does not need a parent key called Inputs
        json_default = {
            "EncodedParameters": json.dumps(_inputs),
            "OperationName": _operation
        }
        # the default REST input in Apriso needs a parent key called Inputs
        if self.ws_type == "REST" :
            json_default = { "Inputs": json_default }
        if self.debug:
            self.logger.debug(f"OperationName = {_operation}")
            self.logger.debug(f"EncodedParameters = {json.dumps(_inputs)}")
            self.logger.debug(f"json_default = {json_default}")
        return json_default

    def get_url(self):
        '''
            purpose: get the webservice access url
            arguments:
                self : [UnitTest] (object instance)
            return: [str] (specific filled webservice access url: REST or SOAP)
        '''
        if self.ws_type == "REST" :
            # in REST it is the endpoint made available when creating the webservice
            url = self.protocol + "://" + self.host + "/" + self.ws_path_rest  + "/" +  self.ws_name 
        else:
            # in SOAP it is necessary to identify the service and the URL query request by parameter: .svc?wsdl
            url = self.protocol + "://" + self.host + "/" + self.ws_path_soap  + "/" +  self.ws_name + ".svc?wsdl"
        if self.debug:
            self.logger.debug(f"url = {url}")
        return url

    def post_webservice(self, _operation, _inputs):
        '''
            purpose: access the webservice by specifying the operation and input
            arguments:
                self : [UnitTest] (object instance)
                _operation : [str] (name of the operation to test)
                _inputs : [dict] (input setup to test operation)
            return: target operation execution response
        '''
        url = self.get_url()
        input_default = self.get_input_default(_operation, _inputs)
        if self.ws_type == "REST" :
            # using requests
            response = requests.post(
                url = url,
                json = input_default
            )
        else:
            # using package zeep
            client = Client(url)
            # the SOAP webservice in Apriso creates 2 operations: Invoke and Invoke_Async
            response = client.service.Invoke( input_default )
        if self.debug:
            self.logger.debug(response)
        return response