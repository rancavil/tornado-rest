from pyrestful.rest import get,post,RestHandler,RestService
from tornado.testing import AsyncHTTPTestCase

import json

class Book:
    title = str
class Person:
    idperson = int
    name = str

class simpleservice(RestHandler):
    @get('/echo/{value}')
    def echo(self,value):
        return value

    @get('/data/{name}',{'format' : 'json'})
    def get_json(self,name):
        return {'name':name}

    @post('/data',{'format' : 'json'})
    def post_json(self,data):
        return data

class bookservice(RestHandler):
    @get('/book/{isbn}',{'produces' : 'application/json'})
    def get_book(self,isbn):
        return {'title' : 'The Quick Python Book','isbn' : isbn}

    @post('/book')
    def post_book(self,data):
        return 'Book isbn {} received'.format(data['isbn'])

class personservice(RestHandler):
    @get('/person',{'format' : 'json'})
    def get_person(self):
        person = Person()
        person.idperson = 1
        person.name = 'Ada'
        return person

    @post('/person',{'format':'json','types' : [Person]},_catch_fire=True)
    def post_person(self,person):
        return {'status' : 'person {} received'.format(person.id)}

class echoservice(RestHandler):
    @get('/test.asp')
    def test_data(self):
        return {'status' : 'Ok'}

    @get('/data.asp/{name}')
    def get_data(self,name):
        return {'hello' : name}

    @post('/data.asp')
    def post_data(self,data):
        return {'received' : data}

class TestService(AsyncHTTPTestCase):
    def get_app(self):
        return RestService([simpleservice,bookservice,personservice,echoservice,])

    def test_get_string(self):
        response = self.fetch('/echo/TEST')
        self.assertEqual(response.code,200)
        self.assertEqual(response.body,b'TEST')

    def test_get_json(self):
        response = self.fetch('/data/tornado')
        response_json = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertDictEqual(response_json,{'name':'tornado'})
        self.assertEqual(response_json['name'],'tornado')

    def test_post_json(self):
        response = self.fetch('/data',method='POST',body=json.dumps({'id' : 123456}),headers={'content-type' : 'application/json'})
        response_json = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertDictEqual(response_json,{'id':123456})

    def test_get_book(self):
        response = self.fetch('/book/978-1617294037')
        response_json = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertIn('Python',response_json['title'])
        self.assertEqual(response_json['isbn'],'978-1617294037')

    def test_post_book(self):
        book = {'isbn' : '978-1617294037','title' : 'The Quick Python Book'}
        response = self.fetch('/book',method='POST',body=json.dumps(book),headers={'content-type' : 'application/json'})
        self.assertEqual(response.code,200)
        self.assertEqual(response.body,b'Book isbn 978-1617294037 received')

    def test_get_person(self):
        response = self.fetch('/person')
        person = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertIn('application/json',response.headers['Content-Type'])
        self.assertEqual(person['idperson'],1)
        self.assertEqual(person['name'],'Ada')

    def test_get_person(self):
        response = self.fetch('/person')
        person = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertIn('application/json',response.headers['Content-Type'])
        self.assertEqual(person['idperson'],1)
        self.assertEqual(person['name'],'Ada')

    def test_post_person(self):
        person = {'id' : 1,'name' : 'Ada'}
        response = self.fetch('/person',method='POST',body=json.dumps(person),headers={'content-type' : 'application/json'})
        response_json = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertIn('application/json',response.headers['Content-Type'])
        self.assertDictEqual(response_json,{'status':'person 1 received'})

    def test_test_1_data(self):
        response = self.fetch('/test.asp')
        data = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertIn('application/json',response.headers['Content-Type'])
        self.assertEqual(data['status'],'Ok')

    def test_test_2_data(self):
        response = self.fetch('/test_asp')
        self.assertEqual(response.code,404)

    def test_get_data(self):
        response = self.fetch('/data.asp/jonnhy')
        data = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertIn('application/json',response.headers['Content-Type'])
        self.assertEqual(data['hello'],'jonnhy')

    def test_post_data(self):
        response = self.fetch('/data.asp',method='POST',body=json.dumps({'id' : 123456}),headers={'content-type' : 'application/json'})
        response_json = json.loads(response.body)
        self.assertEqual(response.code,200)
        self.assertDictEqual(response_json['received'],{'id':123456})

