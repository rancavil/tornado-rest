import httplib
import json

conn = httplib.HTTPConnection("localhost:8881")
conn.request('GET','/datosGET')

resp = conn.getresponse()
data = resp.read()

json_data = json.loads(data)
print json_data['id']+" "+json_data['name']+" "+json_data['method']