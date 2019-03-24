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

import distutils.core

try:
	import setuptools
except ImportError:
	pass

packages=['tornado>=6.0.1','pyconvert']

distutils.core.setup(
	name='pyrestful',
	version = '0.5.1',
	packages=['pyrestful','demos','test'],
	author='Innovaser',
	author_email='rancavil@innovaser.cl',
	install_requires=packages
)
