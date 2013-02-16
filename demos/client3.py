import httplib
import json

conn = httplib.HTTPConnection("localhost:8881")
conn.request('GET','/getdatos?since_id=1&date_since=2013-02-14&value=true')

resp = conn.getresponse()
data = resp.read()
json_data = json.loads(data)
print str(json_data['since_id'])+" "+json_data['name']+" "+json_data['method']+" "+json_data['date']+" "+str(json_data['boolean'])