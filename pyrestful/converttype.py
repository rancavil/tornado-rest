import json
from collections import namedtuple

def json2object(doc,name=None):
    if not isinstance(doc,dict):
        return None
    if name == None:
        name = doc.keys()
    data = json.dumps(doc)
    return json.loads(data,object_hook=lambda d:namedtuple(name,d.keys())(*d.values()))

def object2json(obj):
    if hasattr(obj,'__dict__'):
        return obj.__dict__
    else:
        return None
