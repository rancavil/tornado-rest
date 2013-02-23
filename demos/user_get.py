#!/usr/bin/env python
#
# Copyright 2013 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import httplib
import json

param_id_user = raw_input('Id de usuario : ')

conn = httplib.HTTPConnection("localhost:8881")
conn.request('GET','/user/'+param_id_user)

resp = conn.getresponse()
data = resp.read()
if data != '' or data != None:
	json_data = json.loads(data)
	print json_data