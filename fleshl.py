from urlparse import parse_qs
import re

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
			print "assigning post data to request"
			wsgi_input = pull_environ('wsgi.input').read(self.length)
			print "pulled out wsgi_input"
			self.post_data = parse_qs(wsgi_input)

	def __repr__(self):
		return "<" + self.query + self.method + str(self.length) + \
				", ".join(self.post_data.keys()) + ">"

class Fleshl(object):
	def __init__(self):
		self.routes = {}

	def add_route(self, route):
		def wrapped(func):
			self.routes[route] = func
		return wrapped

	def render(self, template, values):
		tag_search = re.compile("{{ (?P=<tag>) }}")
		'''
		>>> tag_search.search("Lorem \{\{ Ipsum \}\}")
		'''
		

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
		response_headers = [('Content-Type', response[1]), 
		('Content-Length', str(len(response[0])))] 

		start_response(status, response_headers)
		return response[0]

