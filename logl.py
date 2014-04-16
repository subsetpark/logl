from urlparse import parse_qs
import re, os.path, mimetypes
from wsgiref.simple_server import make_server
from pymongo import MongoClient
import render

"""
A very simple web framework modelled on Flask. It features routing and template
rendering with conditional logic and base extension, as well as MongoDB access. 
Do not use this to make an actual website; it will be awful.
"""

class Request(object):
	"""
	Provides useful request information to the web server.
	"""
	def __init__(self, environ):
		self.query = environ.get('PATH_INFO')
		self.q_string = environ.get('QUERY_STRING')
		method = environ.get('REQUEST_METHOD')
		self.method = method.upper() if method else ""
		content_length = environ.get('CONTENT_LENGTH')
		self.length = int(content_length) if content_length else 0

		if self.method == 'GET' and self.q_string:
			self.q_strings = parse_qs(self.q_string)
		else:
			self.q_strings = ""

		if self.method == 'POST':
			wsgi_input = environ['wsgi.input'].read(self.length)
			self.post_data = parse_qs(wsgi_input)

	def __repr__(self):
		return "<" + self.query + ", " + self.method + ", " + str(self.length) + ", " + str(self.post_data) + str(self.q_strings) + ">"

class Response(object):
	"""
	Builds a response object, usually out of an html template and the
	necessary args for rendering. Optionally the content can be set
	manually in the case of non-html stuff like favicons
	"""

	def __init__(self, context, content=None, template=None, content_type=None):

		self.content = content if content else render.render(template, context)
		if content_type:
			self.type = content_type
		else:
			if "html" in template:
				self.type = 'text/html'
			else:
				self.type = 'text/plain'
		self.length = str(len(self.content)) if isinstance(self.content, str) else "0"

class Context(object):

	def __init__(self):
		self.cons = {}
		self.replaces = {}

	def flush(self):
		self.cons = {}
		self.replaces = {}

class Logl(object):
	""" A lightweight flask clone web framework
	"""
	def __init__(self):
		self.routes = {}
		self.db_client = MongoClient('localhost', 27017)
		self.context = Context()

	def add_route(self, route):
		def wrapped(func):
			self.routes[route] = func
		return wrapped

	def run(self, environ, start_response):
		self.request = Request(environ)
		self.context.flush()
		# If the URL is a file that exists, use it to create a new response
		if os.path.isfile(self.request.query[1:]):
			with open(self.request.query[1:]) as f:
				response = Response(self, content=f.read(), content_type=str(mimetypes.guess_type(self.request.query)))
		# Otherwise look up the route
		else:
			response = self.routes[self.request.query]()
		status = '200 OK' if response else '404 NOT FOUND'
		response_headers = [('Content-Type', response.type), 
							('Content-Length', response.length)] 
		start_response(status, response_headers)
		return response.content

	def response(self, **args):
		return Response(self.context, **args)

	def add_con(self, key, value):
		self.context.cons[key] = value

	def add_replace(self, key, value):
		self.context.replaces[key] = value

	def start(self, host, port):
		server = make_server(host, port, self.run)
		server.serve_forever()
