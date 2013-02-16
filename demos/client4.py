import httplib
import xml.dom.minidom

conn = httplib.HTTPConnection("localhost:8881")
conn.request('GET','/datosXML?date_since=2013-02-12')

resp = conn.getresponse()
data = resp.read()
print data
