#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask-Autoversion
-----------------
Automatically add query parameters to static file paths. When actively 
developing a web application, you may experience issues with browsers 
caching your static content. With this extension you can easily use the 
function in your templates that will update the query added on to the 
file path to bust the browser cache. Here's an example usage::
	<link rel="stylesheet" href="{{ static_autoversion('app.css') }}">
Links
`````
* `development version
  <http://github.com/bmcculley/flask-autoversion/>`_
"""
from setuptools import setup
import unittest

def autoversion_test_suite():
	test_loader = unittest.TestLoader()
	test_suite = test_loader.discover('tests', pattern='test_*.py')
	return test_suite

def fread(filepath):
	with open(filepath, 'r') as f:
		return f.read()

setup(
	name='Flask-Autoversion',
	version='0.2.0',
	url='http://github.com/bmcculley/flask-autoversion',
	license='BSD',
	author='bmcculley',
	author_email='fva@pypi.e42.xyz',
	description='Add query parameters to static file paths.',
	long_description=fread('README.md'),
	long_description_content_type='text/markdown',
	packages=[
		'flaskext',
		'flaskext.autoversion',
	],
	namespace_packages=['flaskext'],
	zip_safe=False,
	platforms='any',
	install_requires=[
		'setuptools',
		'Flask',
	],
	test_suite='setup.autoversion_test_suite',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development :: Libraries :: Python Modules'
	]
)