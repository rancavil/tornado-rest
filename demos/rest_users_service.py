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
import pyrestful.rest

from pyrestful.rest  import get, post

class MyRestService(pyrestful.rest.RestHandler):
	database = dict()
	
	@get(_resource='user/:id_user',_format="JSON",_types=[str])
	def get_user(self, id_user):
		d = None
		if id_user in self.database:
			d = self.database[id_user]
		else:
			d = {'status':'NOk'}
		return d
	
	@post(_resource='user',_format="JSON",_types=[str,str,int])
	def insert_user(self, id_user, name, age):
		data = {'id_user':id_user, 'name':name, 'age':age}
		self.database[id_user] = data
		
		result = {'status':'Ok'}
		return result
		
if __name__ == '__main__':
	try:
		app = pyrestful.rest.RestService(MyRestService)
		app.listen(8881)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print "\nStop the service"