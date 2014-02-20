from fleshl import Fleshl
from wsgiref.simple_server import make_server


app = Fleshl()

@app.add_route('/')
def index():
	return ("You asked for %s." % app.request.query, 'text/plain')
	
@app.add_route('/form')
def form():
	html = """
	<html>
	<body>
	<form method="post" action="/form">
		<p>
			<input type="text" name="arg">
			<input type="submit" value="Submit">
		</p>
	</form>
	<p>
	You entered %s.
	</p>
	</html>
	"""
	
	if 'arg' not in app.request.post_data:
		readback = "Give some data!"
	elif app.request.post_data['arg']:
		readback = app.request.post_data['arg'][0]
	else:
		readback = "No information"
	return (html % readback, 'text/html')


httpd = make_server('localhost', 5000, app.run)
httpd.serve_forever()