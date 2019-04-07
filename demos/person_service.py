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

class Person(object):
	idperson = int 
	name = str

class PersonService(pyrestful.rest.RestHandler):
    @get('/person/{idperson}',{'format':'json'})
    def getPerson(self, idperson):
        p = Person()
        p.idperson = int(idperson)
        p.name = 'Mr.Robot'
        return p

    @post('/person',{'format':'json'},_catch_fire=True)
    def postPerson(self,person):
        return {'status':'person OK', 'person' : person}

if __name__ == '__main__':
    try:
        print("Start the service")
        app = pyrestful.rest.RestService([PersonService])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")
