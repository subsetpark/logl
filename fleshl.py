from urlparse import parse_qs
import re
from wsgiref.simple_server import make_server

class Request(object):
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

		if self.method is 'GET' and '?' in self.query:
			self.q_strings = self.query[self.query.index('?'):-1]

		if 'POST' in self.method and self.length:
			wsgi_input = pull_environ('wsgi.input').read(self.length)
			self.post_data = parse_qs(wsgi_input)

	def __repr__(self):
		return "<" + self.query + self.method + str(self.length) + \
				", ".join(self.post_data.keys()) + ">"

class Response(object):
	def __init__(self, content=None, template=None, content_type=None, **replaces):
		if content:
			self.content = content
		else:
			self.content = render(template, **replaces)
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
	def __init__(self):
		self.routes = {}

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
		response = self.routes[environ.get('PATH_INFO')]()

		if response:
			status = '200 OK'
		else:
			status = '404 NOT FOUND'
		response_headers = [('Content-Type', response.type), 
							('Content-Length', response.length)] 

		start_response(status, response_headers)
		return response.content


def render(template=None, **replaces):	
	if not template:
		return None

	text = ""
	filename = "templates/" + template

	with open(filename) as f:
		text = f.read()
		for replace in replaces.keys():
			arg_search = re.compile("{{" + replace + "}}")
			text = re.sub(arg_search, replaces[replace], text)
	return text

def spin_server(host, port, app_func):
	server = make_server(host, port, app_func)
	return server