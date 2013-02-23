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

import tornado.ioloop
import tornado.web
import xml.dom.minidom
import inspect

from pyrestful.types import boolean, date

def convert(value, type):
	""" Convert / Cast function """
	if issubclass(type,str) and not (value.upper() in ['FALSE','TRUE']):
		return str(value)
	elif issubclass(type,unicode):
		return unicode(value)
	elif issubclass(type,int):
		return int(value)
	elif issubclass(type,float):
		return float(value)
	elif issubclass(type,boolean) and (value.upper() in ['FALSE','TRUE']):
		if str(value).upper() == 'TRUE': return True
		elif str(value).upper() == 'FALSE': return False
	else:
		return value

def config(func,method,**kwparams):
	""" Decorator config function """
	format = None
	types  = None
	if len(kwparams):
		resource = kwparams['_resource']
		if '_format' in kwparams:
			format = kwparams['_format']
		else:
			format = 'JSON'
		if '_types' in kwparams:
			types = kwparams['_types']
		
	def operation(*args,**kwargs):
		return func(*args,**kwargs)
	
	uri = resource.split('/')
	service_name  = uri[0]
	service_param = None
	if len(uri) >= 2:
		service_param = uri[1]
	
	operation.func_name      = func.func_name
	operation._service_name  = service_name
	operation._service_param = service_param
	operation._params        = inspect.getargspec(func).args[1:]
	operation._method        = method
	operation._format        = format
	operation._types         = types

	return operation

def get(*params, **kwparams):
	""" Decorator for config a python function like a Rest GET verb	"""
	def method(f):
		return config(f,'GET',**kwparams)
	
	return method
	
def post(*params, **kwparams):
	""" Decorator for config a python function like a Rest POST verb	"""
	def method(f):
		return config(f,'POST',**kwparams)
	
	return method

class RestHandler(tornado.web.RequestHandler):
	def get(self):
		""" Executes get method """
		self._exe('GET')

	def post(self):
		""" Executes post method """
		self._exe('POST')
	
	def _get_params(self, method, param=None):
		""" Normalizes the parameters incoming in the request post or get """
		if method.upper() == 'GET':
			if param != None:
				req_parse = self.request.path.split('/')
				value     = None
				if len(req_parse) >= 3:
					value = str(req_parse[2])
				query = "%s=%s"%(param.replace(':',''),value)
				if len(self.request.query) > 0:
					query = query+"&"+self.request.query
				
				return query
			else:
				return self.request.query
		elif method.upper() == 'POST':
			query = ''
			for name in self.request.arguments.keys():
				query += name+'='+self.get_argument(name)+'&'
				
			return query[0:len(query)-1]
			
	def _parse_params(self, params):
		""" Parses the incoming params, generating the dictionary with param name : value """
		parlist = params.split('&')
		pardict = dict()
		for p in parlist:
			d = p.split('=')
			if len(d) >= 2:
				pardict[str(d[0])] = str(d[1])
			
		return pardict

	def _genera_params(self, types, params, params_from_request):
		""" Generates the parameters for the python function. 
		    If there are not types (types == None) all parameters
			are convert to str
		"""
		i = 0
		pars = []
		for p in params:
			if p in params_from_request:
				if types != None:
					pars.append(convert(params_from_request[p],types[i]))
					i+=1
				else:
					pars.append(str(params_from_request[p]))				
			else:
				pars.append(None)
				
		return pars

	def _verify_rest_operation(self,operation,method,path):
		""" Verifies what the attributes are validates """
		if callable(operation) and self._get_attr(operation,'_method') == method and self._get_attr(operation,'_service_name') == path:
			return True
		else:
			return False

	def _get_attr(self,operation,attr_name):
		""" Verifies if the operation has the attribute and get its value """
		if hasattr(operation,attr_name):
			return getattr(operation,attr_name)
		else:
			return None
	
	def _exe(self, method):
		""" Executes the python function for the Rest Service """
		path   = self.request.path.split('/')[1]
		
		for operations in dir(self):
			operation = getattr(self,operations)

			if self._verify_rest_operation(operation,method,path):
				params = self._get_params(method,getattr(operation,'_service_param'))
				format = self._get_attr(operation,'_format')

				if format == 'JSON':
					self.set_header("Content-Type","application/json")
				elif format == 'XML':
					self.set_header("Content-Type","text/xml")

				types  = getattr(operation,'_types')
				params = getattr(operation,'_params')
				params_from_request = None
				if len(params) > 0:
					params_from_request = self._parse_params(params)
					
				pars = self._genera_params(types,params,params_from_request)
				
				response = operation(*pars)

				if isinstance(response,dict) or isinstance(response,xml.dom.minidom.Document):
					self.write(response)
				else:
					raise tornado.web.HTTPError(500,'Internal Server Error : response is not %s document'%format)

	@classmethod
	def get_services(self):
		""" Generates the resources (uri) to deploy the Rest Services """
		services = []
		for f in dir(self):
			o = getattr(self,f)
			if callable(o) and hasattr(o,'_service_name'):
				services.append(getattr(o,'_service_name'))
		return services
						
class RestService(tornado.web.Application):
	""" Class to create Rest services in tornado web server
	"""
	def __init__(self, rest):
		services = rest.get_services()
		svs = []
		for s in services:
			svs.append((r'/'+s+'[/0-9a-zA-Z]*',rest))
		tornado.web.Application.__init__(self,svs)		
