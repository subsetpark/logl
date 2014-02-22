from urlparse import parse_qs
import re, os.path, mimetypes
from wsgiref.simple_server import make_server
import render
from pymongo import MongoClient

class Request(object):
	"""
	Provides useful request information to the web server.
	"""
	def __init__(self, environ):
		def pull_environ(key):
			try:
				return environ[key]
			except KeyError:
				return None

		self.query = pull_environ('PATH_INFO')
		self.method = pull_environ('REQUEST_METHOD').upper()
		content_length = pull_environ('CONTENT_LENGTH')
		if content_length:
			self.length = int(content_length)

		self.post_data = {}
		self.q_strings = {}

		if 'GET' in self.method and '?' in self.query:
			self.q_strings = self.query[self.query.index('?'):-1]

		if 'POST' in self.method and self.length:
			wsgi_input = pull_environ('wsgi.input').read(self.length)
			self.post_data = parse_qs(wsgi_input)

	def __repr__(self):
		return "<" + self.query + self.method + str(self.length) + \
				", ".join(self.post_data.keys()) + ">"

class Response(object):
	"""
	Builds a response object, usually out of an html template and the
	necessary args for rendering. Optionally the content can be set
	manually in the case of non-html stuff like favicons
	"""

	def __init__(self, content=None, template=None, content_type=None, **replaces):
		if content:
			self.content = content
		else:
			self.content = render.render(template, **replaces)
		if content_type:
			self.type = content_type
		else:
			if "html" in template:
				self.type = 'text/html'
			else:
				self.type = 'text/plain'
		
		if isinstance(self.content, str):
			self.length = str(len(self.content))
		else:
			self.length = str(0)

class Fleshl(object):
	""" A lightweight flask clone web framework
	"""
	def __init__(self):
		self.routes = {}
		self.db_client = MongoClient('localhost', 27017)

	def add_route(self, route):
		def wrapped(func):
			self.routes[route] = func
		return wrapped

	def run(self, environ, start_response):
		# Run the function associated with the URL we pull from
		# environ
		
		import doctest
		doctest.testmod()
		
		self.request = Request(environ)
		
		# If the URL is a file that exists, use it to create a new response
		if os.path.isfile(self.request.query[1:]):
			with open(self.request.query[1:]) as f:
				response = Response(content=f.read(), content_type=str(mimetypes.guess_type(self.request.query)))
		# Otherwise look up the route
		else:
			response = self.routes[self.request.query]()

		if response:
			status = '200 OK'
		else:
			status = '404 NOT FOUND'
		response_headers = [('Content-Type', response.type), 
							('Content-Length', response.length)] 

		start_response(status, response_headers)
		return response.content

def spin_server(host, port, app_func):
	"""
	A pretty useless wrapper for wsgi's make_server, so client apps
	Don't have to import wsgi
	"""

	server = make_server(host, port, app_func)
	return server