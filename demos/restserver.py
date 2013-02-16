#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import pyrestful.rest
import xml.dom.minidom

from pyrestful.rest  import get, post
from pyrestful.types import boolean, date

class MyRestService(pyrestful.rest.RestHandler):
	@get(_resource="datosGET",_format="JSON")
	def datosGET(self):
		d = {"id":"1021121","name":"Mattel","method":"Data from a Get"}
		return d

	@get(_resource="getdatos",_format="JSON",_types=[int,str,boolean])
	def getdatos(self,since_id,date_since,value):
		if value == None:
			value = 'None'
		d = {"since_id":since_id,"name":"Matchbox","method":"Data from a Get","date":date_since,"boolean":value}
		return d
		
	@post(_resource="datosPOST",_format="JSON", _types=[int,str,int])
	def datosPOST(self,user_id,name,age):
		d = {"id":user_id,"name":name,"age":age,"method":"Data from a Post"}
		return d

	@get(_resource="datosXML",_format="XML")
	def datosXML(self,date_since):
		xmldoc = xml.dom.minidom.parseString('<Documento><nro>1</nro><texto>Mensaje con datos</texto><fecha>'+date_since+'</fecha></Documento>')
		
		return xmldoc
		
if __name__ == '__main__':
	try:
		app = pyrestful.rest.RestService(MyRestService)
		app.listen(8881)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print "\nStop the service"