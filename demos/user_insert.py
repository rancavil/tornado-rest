import httplib
import json
import urllib

id_user = raw_input('Id de usuario : ')
name    = raw_input('Nombre        : ')
age     = raw_input('Edad          : ')

if len(id_user) == 0 and len(name) == 0 and len(age) == 0:
	print 'Debe ingresar todos los datos solicitados!!!'
else:
	params = urllib.urlencode({'id_user':str(id_user),'name':str(name),'age':int(age)})
	headers = {"Content-type": "application/x-www-form-urlencoded"}
	conn = httplib.HTTPConnection("localhost:8881")
	conn.request('POST','/user',params,headers)

	resp = conn.getresponse()
	data = resp.read()
	json_data = json.loads(data)
	print json_data