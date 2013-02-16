import httplib
import json

conn = httplib.HTTPConnection("localhost:8881")
conn.request('GET','/echo?name=rodrigo&age=30')

resp = conn.getresponse()
data = resp.read()
json_data = json.loads(data)
print json_data