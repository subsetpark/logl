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
		
		# import pdb
		# pdb.set_trace()
		response_body = self.routes[environ.get('PATH_INFO')]()
		
		if response_body:
			status = '200 OK'
		else:
			status = '404 NOT FOUND'
		response_headers = [('Content-Type', 'text/plain'), 
		('Content-Length', str(len(response_body)))] 
		
		start_response(status, response_headers)
		return response_body
