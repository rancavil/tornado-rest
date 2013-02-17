#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornadows.rest
		
from tornadows.rest  import get, post
		
class MyRestService(tornadows.rest.RestHandler):
	@get(_resource="echo",_format="JSON",_types=[str,int])
	def echo(self,name,age):
		d = {"message":{"name":name,"age":age}}
		return d
		
if __name__ == '__main__':
	try:
		app = tornadows.rest.RestService(MyRestService)
		app.listen(8881)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print "\nStop the service"