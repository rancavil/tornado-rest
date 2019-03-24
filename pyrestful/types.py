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

def convert_primitive(value):
        if isinstance(value,unicode):
            return value
        elif isinstance(value,str):
            value = unicode(value,'utf-8')
            if value.isdigit():
                return long(value)
            elif value.isalnum():
                if value.upper() == 'TRUE':
                    return True
                if value.upper() == 'FALSE':
                    return False
                return value

def convert(value, data_type):
	""" Convert / Cast function """
	if issubclass(data_type,str) and not (value.upper() in ['FALSE','TRUE']):
		return value.decode('utf-8')
	elif issubclass(data_type,unicode):
		return convert_primitive(value)
	elif issubclass(data_type,int):
		return int(value)
	elif issubclass(data_type,long):
		return long(value)
	elif issubclass(data_type,float):
		return float(value)
	elif issubclass(data_type,boolean) and (value.upper() in ['FALSE','TRUE']):
		if str(value).upper() == 'TRUE': return True
		elif str(value).upper() == 'FALSE': return False
	else:
		return value
