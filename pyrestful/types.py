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

# -*- coding: utf-8 -*-

import sys
from datetime import date
boolean = str

if sys.version_info > (3,):
	long = int
	unicode = str
	str = bytes

def convert(value, type):
	""" Convert / Cast function """
	if issubclass(type,str) and not (value.upper() in ['FALSE','TRUE']):
		return value.decode('utf-8')
	elif issubclass(type,unicode):
		return unicode(value)
	elif issubclass(type,int):
		return int(value)
	elif issubclass(type,long):
		return long(value)
	elif issubclass(type,float):
		return float(value)
	elif issubclass(type,boolean) and (value.upper() in ['FALSE','TRUE']):
		if str(value).upper() == 'TRUE': return True
		elif str(value).upper() == 'FALSE': return False
	else:
		return value
