import pyrest
import json

r = pyrest.rest()
response = r.urlrequest("http://localhost:8881/getdatos?since_id=111111&date_since=2012-12-31&value=true")
json_data = response.body
print 'since_id : %d'%json_data['since_id']
print 'name     : %s'%json_data['name']
print 'date     : %s'%json_data['date']
print 'boolean  : %s'%json_data['boolean']