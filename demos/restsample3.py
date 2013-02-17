#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornadows.rest
import xml.dom.minidom

from tornadows.rest  import get, post

class MyRestService(tornadows.rest.RestHandler):
	database = dict()
	
	@get(_resource='user/:id_user',_format="JSON",_types=[str,unicode])
	def get_user(self, id_user,access_token):
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
		app = tornadows.rest.RestService(MyRestService)
		app.listen(8881)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print "\nStop the service"