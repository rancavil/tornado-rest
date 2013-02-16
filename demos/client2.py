import httplib
import json
import urllib

params = urllib.urlencode({'user_id':1,'name':'rodrigo','age':39})
headers = {"Content-type": "application/x-www-form-urlencoded"}
conn = httplib.HTTPConnection("localhost:8881")
conn.request('POST','/datosPOST',params,headers)

resp = conn.getresponse()
data = resp.read()
json_data = json.loads(data)
print json_data