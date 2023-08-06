# -*- coding: utf-8 -*-
"""
	flaskext.autoversion
	~~~~~~~~~~~~~~~~~~~~
	Add query parameters to static file paths.
	:copyright: (c) 2020 by bmcculley.
	:license: BSD, see LICENSE for more details
"""
from flask import url_for
import os

__all__ = ['Autoversion']

class Autoversion(object):

	def __init__(self, app, **options):
		self.autoversion_app_context = app
		app.jinja_env.globals.update(
				static_autoversion=self.static_autoversion)

	def static_autoversion(self, filename):
		if ( hasattr(self.autoversion_app_context, 'autoversion') and 
				self.autoversion_app_context.autoversion ):
			fullpath = os.path.join(
					self.autoversion_app_context.root_path + \
					self.autoversion_app_context.static_url_path, 
					filename)
			try:
				timestamp = str(os.path.getmtime(fullpath))
			except OSError:
				return url_for('static', filename=filename)
			return url_for('static', filename=filename, ts=timestamp)
		else:
			return url_for('static', filename=filename)
