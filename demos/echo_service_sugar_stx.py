import tornado.ioloop
import pyrestful.rest

from pyrestful import mediatypes
from pyrestful.rest import get

class EchoService(pyrestful.rest.RestHandler):
    @get("/echo/{name}",{'format':'xml'},_catch_fire=True)
    def sayHello(self, name):
         return {"Hello":name}

if __name__ == '__main__':
    try:
         print("Start the echo service")
         app = pyrestful.rest.RestService([EchoService])
         app.listen(8080)
         tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
         print("\nStop the echo service")
