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

from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete

class Book(object):
	isbn = int
	title = str

class BookResource(pyrestful.rest.RestHandler):
	@get(_path="/books/json/{isbn}", _types=[int], _produces=mediatypes.APPLICATION_JSON)
	def getBookJSON(self, isbn):
		book = Book()
		book.isbn = isbn
		book.title = "My book for isbn "+str(isbn)

		return book

	@get(_path="/books/xml/{isbn}", _types=[int], _produces=mediatypes.APPLICATION_XML)
	def getBookXML(self, isbn):
		book = Book()
		book.isbn = isbn
		book.title = "My book for isbn "+str(isbn)

		return book

	@post(_path="/books/xml",_types=[Book],_consumes=mediatypes.APPLICATION_XML, _produces=mediatypes.APPLICATION_XML)
	def postBookXML(self, book):
		""" this is an echo...returns the same xml document """
		return book

	@post(_path="/books/json",_types=[Book],_consumes=mediatypes.APPLICATION_JSON, _produces=mediatypes.APPLICATION_JSON)
	def postBookJSON(self, book):
		""" this is an echo...returns the same json document """
		return book

	@post(_path="/books",_types=[Book])
	def postBook(self, book):
		""" this is an echo, returns json or xml depending of request content-type """
		return book

if __name__ == '__main__':
	try:
		print("Start the service")
		app = pyrestful.rest.RestService([BookResource])
		http_server = tornado.httpserver.HTTPServer(app)
		http_server.listen(8080)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print("\nStop the service")
