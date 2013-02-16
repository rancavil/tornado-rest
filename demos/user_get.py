import httplib
import json

par = raw_input('Id de usuario :')

conn = httplib.HTTPConnection("localhost:8881")
conn.request('GET','/user/'+par+'?access_token=fdsX2121hw3211232')

resp = conn.getresponse()
data = resp.read()
if data != '' or data != None:
	json_data = json.loads(data)
	print json_data