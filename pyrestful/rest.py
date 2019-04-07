#!/usr/bin/env python
#
# Copyright 2013 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# -*- coding: utf-8 -*-

import tornado
import tornado.ioloop
import tornado.web
import tornado.wsgi
import xml.dom.minidom
import inspect
import re
import json
import sys

from pyrestful import mediatypes, types
from pyconvert.pyconv import convertXML2OBJ, convert2XML, convertJSON2OBJ, convert2JSON

class PyRestfulException(Exception):
	""" Class for PyRestful exceptions """
	def __init__(self,message):
		self.message = message
	def __str__(self):
		return repr(self.message)

def convert_format(data_format):
        if data_format == 'json':
            return mediatypes.APPLICATION_JSON
        elif data_format == 'xml':
            return mediatypes.APPLICATION_XML
        else:
            return None

def config(func,method,*params,**kwparams):
	""" Decorator config function """
	path     = None
	produces = None
	consumes = None
	types    = None
	manual_response = None
	catch_fire = False

	if len(params) >= 1 and (len(kwparams) == 1 or len(kwparams) == 0):
		path = params[0] # 1st param _path
		if len(params) == 2 and isinstance(params[1],dict): # content-type
                        if 'consumes' in params[1].keys():
                                consumes = params[1]['consumes']
                        if 'produces' in params[1].keys():
                                produces = params[1]['produces']
                        if 'format' in params[1].keys():
                                consumes = convert_format(params[1]['format'])
                                produces = convert_format(params[1]['format'])
                        if 'types' in params[1].keys() and isinstance(params[1]['types'],list):
                                types = params[1]['types']

		if '_catch_fire' in kwparams:
			catch_fire = kwparams['_catch_fire']

	if len(params) == 0 and len(kwparams):
		path = kwparams['_path']
		if '_produces' in kwparams:
			produces = kwparams['_produces']
		if '_consumes' in kwparams:
			consumes = kwparams['_consumes']
		if '_types' in kwparams:
			types = kwparams['_types']
		if '_manual_response' in kwparams:
			manual_response = kwparams['_manual_response']
		if '_catch_fire' in kwparams:
			catch_fire = kwparams['_catch_fire']

	def operation(*args,**kwargs):
		return func(*args,**kwargs)

	operation.func_name       = func.__name__
	operation._func_params    = inspect.getargspec(func).args[1:]
	operation._types          = types or [str]*len(operation._func_params)
	operation._service_name   = re.findall(r'(?<=/)[a-zA-z0-9\.\-]+',path)
	operation._service_params = re.findall(r'(?<={)\w+',path)
	operation._method         = method
	operation._produces       = produces
	operation._consumes       = consumes
	operation._query_params   = re.findall(r'(?<=<)\w+',path)
	operation._path           = path
	operation._manual_response = manual_response
	operation._catch_fire = catch_fire
	
	if not operation._produces in [mediatypes.APPLICATION_JSON,mediatypes.APPLICATION_XML,mediatypes.TEXT_XML,mediatypes.TEXT_PLAIN, None]:
		raise PyRestfulException('The media type used do not exist : '+operation.func_name)

	return operation

def get(*params, **kwparams):
	""" Decorator for config a python function like a Rest GET verb	"""
	def method(f):
		return config(f,'GET',*params,**kwparams)
	return method
	
def post(*params, **kwparams):
	""" Decorator for config a python function like a Rest POST verb """
	def method(f):
		return config(f,'POST',*params,**kwparams)
	return method

def put(*params, **kwparams):
	""" Decorator for config a python function like a Rest PUT verb	"""
	def method(f):
		return config(f,'PUT',*params,**kwparams)
	return method

def patch(*params, **kwparams):
        """ Decorator for config a python function like a Rest PATCH verb """
        def method(f):
            return config(f, 'PATCH',*params, **kwparams)
        return method

def delete(*params, **kwparams):
	""" Decorator for config a python function like a Rest PUT verb	"""
	def method(f):
		return config(f,'DELETE',*params,**kwparams)
	return method

class RestHandler(tornado.web.RequestHandler):
	def get(self):
		""" Executes get method """
		self._exe('GET')

	def post(self):
		""" Executes post method """
		self._exe('POST')

	def put(self):
		""" Executes put method """
		self._exe('PUT')

	def patch(self):
		""" Executes patch method """
		self._exe('PATCH')

	def delete(self):
		""" Executes put method """
		self._exe('DELETE')

	def _exe(self, method):
		""" Executes the python function for the Rest Service """
		request_path = self.request.path
		path = request_path.split('/')
		services_and_params = list(filter(lambda x: x!='',path))
		content_type = None
		if 'Content-Type' in self.request.headers.keys():
			content_type = self.request.headers['Content-Type']

		# Get all funcion names configured in the class RestHandler
		functions    = list(filter(lambda op: hasattr(getattr(self,op),'_service_name') == True and inspect.ismethod(getattr(self,op)) == True, dir(self)))
		# Get all http methods configured in the class RestHandler
		http_methods = list(map(lambda op: getattr(getattr(self,op),'_method'), functions))

		if method not in http_methods:
			raise tornado.web.HTTPError(405,'The service not have %s verb'%method)
		if path[1] not in list(op._path.split('/')[1] for op in list(map(lambda o: getattr(self,o),functions))):
			raise tornado.web.HTTPError(404,'404 Not Found {}'.format(path[1]))
		for operation in list(map(lambda op: getattr(self,op), functions)):
			service_name          = getattr(operation,'_service_name')
			service_params        = getattr(operation,'_service_params')
			# If the _types is not specified, assumes str types for the params
			params_types          = getattr(operation,"_types") or [str]*len(service_params)
			params_types          = params_types + [str]*(len(service_params)-len(params_types))
			produces              = getattr(operation,'_produces')
			consumes              = getattr(operation,'_consumes')
			services_from_request = list(filter(lambda x: x in path,service_name))
			query_params          = getattr(operation,'_query_params')
			manual_response       = getattr(operation,'_manual_response')
			catch_fire	      = getattr(operation,'_catch_fire')

			if operation._method == self.request.method and service_name == services_from_request and len(service_params) + len(service_name) == len(services_and_params):
				try:
					params_values = self._find_params_value_of_url(service_name,request_path) + self._find_params_value_of_arguments(operation)
					p_values      = self._convert_params_values(params_values, params_types)

					if consumes == None and content_type != None:
                                                consumes = content_type
					if consumes == mediatypes.APPLICATION_XML:
						param_obj = None
						body = self.request.body
						if sys.version_info > (3,):
							body = str(body,'utf-8')
						if len(body) >0 and params_types[0] in [str]:
							param_obj = xml.dom.minidom.parseString(body)
						elif len(body)>0 :
							param_obj = convertXML2OBJ(params_types[0],xml.dom.minidom.parseString(body).documentElement)
						if param_obj != None:
						        p_values.append(param_obj)
					elif consumes == mediatypes.APPLICATION_JSON:
						param_obj = None
						body = self.request.body
						if sys.version_info > (3,):
							body = str(body,'utf-8')
						if len(body)>0 and params_types[0] in [dict,str]:
							param_obj = json.loads(body)
						elif len(body)>0 :
							param_obj = convertJSON2OBJ(params_types[0],json.loads(body))
						if param_obj != None:
						        p_values.append(param_obj)
					elif consumes == mediatypes.TEXT_PLAIN:
						body = self.request.body
						if len(body) >= 1:
						        if sys.version_info > (3,):
							        body = str(body,'utf-8')
						        if isinstance(body,str):
						   	        param_obj = body
						        else:
							        param_obj = convertJSON2OBJ(params_types[0],json.loads(body))
						        p_values.append(param_obj)
                                                
					response = operation(*p_values)
				
					if response == None:
						return

					if produces != None:
                                                self.set_header('Content-Type',produces)

					if manual_response:
						return

					if (produces == mediatypes.APPLICATION_JSON or produces == None) and hasattr(response,'__module__'):
						response = convert2JSON(response)
					elif produces == mediatypes.APPLICATION_XML and hasattr(response,'__module__') and not isinstance(response,xml.dom.minidom.Document):
						response = convert2XML(response)

					if produces == None and (isinstance(response,dict) or isinstance(response,str)):
						self.write(response)
						self.finish()
					elif produces == None and isinstance(response,list):
						self.write(json.dumps(response))
						self.finish()
					elif produces == mediatypes.TEXT_PLAIN and isinstance(response,str):
						self.write(response)
						self.finish()
					elif produces == mediatypes.APPLICATION_JSON and isinstance(response,dict):
						self.write(response)
						self.finish()
					elif produces == mediatypes.APPLICATION_JSON and isinstance(response,list):
						self.write(json.dumps(response))
						self.finish()
					elif produces in [mediatypes.APPLICATION_XML,mediatypes.TEXT_XML] and isinstance(response,xml.dom.minidom.Document):
						self.write(response.toxml())
						self.finish()
					else:
						self.gen_http_error(500,'Internal Server Error : response is not %s document'%produces)
						if catch_fire == True:
							raise PyRestfulException('Internal Server Error : response is not %s document'%produces)
				except Exception as detail:
					self.gen_http_error(500,'Internal Server Error : %s'%detail)
					if catch_fire == True:
						raise PyRestfulException(detail)

	def _find_params_value_of_url(self,services,url):
		""" Find the values of path params """
		values_of_query = list()
		i = 0
		url_split = url.split('/')
		values = [item for item in url_split if item not in services and item != '']
		for v in values:
			if v != None:
				values_of_query.append(v)
				i+=1
		return values_of_query

	def _find_params_value_of_arguments(self, operation):
		values = []
		if len(self.request.arguments) > 0:
			a = operation._service_params
			b = operation._func_params
			params = [item for item in b if item not in a]
			for p in params:
				if p in self.request.arguments.keys():
					v = self.request.arguments[p]
					values.append(v[0])
				else:
					values.append(None)
		elif len(self.request.arguments) == 0 and len(operation._query_params) > 0:
			values = [None]*(len(operation._func_params) - len(operation._service_params))
		return values

	def _convert_params_values(self, values_list, params_types):
		""" Converts the values to the specifics types """
		values = list()
		i = 0
		for v in values_list:
			if v != None:
				values.append(types.convert(v,params_types[i]))
			else:
				values.append(v)
			i+=1
		return values

	def gen_http_error(self,status,msg):
		""" Generates the custom HTTP error """
		self.clear()
		self.set_status(status)
		self.write('<html><body>'+str(msg)+'</body></html>')
		self.finish()

	@classmethod
	def get_services(self):
		""" Generates the resources (uri) to deploy the Rest Services """
		services = []
		for f in dir(self):
			o = getattr(self,f)
			if callable(o) and hasattr(o,'_service_name'):
				services.append(getattr(o,'_service_name'))
		return services

	@classmethod
	def get_paths(self):
		""" Generates the resources from path (uri) to deploy the Rest Services """
		paths = []
		for f in dir(self):
			o = getattr(self,f)
			if callable(o) and hasattr(o,'_path'):
				paths.append(getattr(o,'_path'))
		return paths

	@classmethod
	def get_handlers(self):
		""" Gets a list with (path, handler) """
		svs = []
		paths = self.get_paths()
		for p in paths:
			s = re.sub(r'(?<={)\w+}','.*',p).replace('{','')
			o = re.sub(r'(?<=<)\w+','',s).replace('<','').replace('>','').replace('&','').replace('?','')
			svs.append((o,self))

		return svs

class RestService(tornado.web.Application):
	""" Class to create Rest services in tornado web server """
	resource = None
	def __init__(self, rest_handlers, resource=None, handlers=None, default_host='', transforms=None, **settings):
		restservices = []
		self.resource = resource
		for r in rest_handlers:
			svs = self._generateRestServices(r)
			restservices += svs
		if handlers != None:
			restservices += handlers
		tornado.web.Application.__init__(self, restservices, default_host, transforms, **settings)

	def _generateRestServices(self,rest):
		svs = []
		paths = rest.get_paths()
		for p in paths:
			s = re.sub(r'(?<={)\w+}','.*',p).replace('{','')
			o = re.sub(r'(?<=<)\w+','',s).replace('<','').replace('>','').replace('&','').replace('?','')
			svs.append((o,rest,self.resource))

		return svs

if tornado.version[0] < '6':
    class WSGIRestService(tornado.wsgi.WSGIApplication):
        """ Class to create WSGI Rest services in tornado web server """
        resource = None
        def __init__(self, rest_handlers, resource=None, handlers=None, default_host='', **settings):
            restservices = []
            self.resource = resource
            for r in rest_handlers:
                svs = self._generateRestServices(r)
                restservices += svs
                if handlers != None:
                    restservices += handlers
                    tornado.wsgi.WSGIApplication.__init__(self, restservices, default_host, **settings)

        def _generateRestServices(self,rest):
            svs = []
            paths = rest.get_paths()
            for p in paths:
                s = re.sub(r'(?<={)\w+}','.*',p).replace('{','')
                o = re.sub(r'(?<=<)\w+','',s).replace('<','').replace('>','').replace('&','').replace('?','')
                svs.append((o,rest,self.resource))

            return svs
