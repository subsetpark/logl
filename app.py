from fleshl import Fleshl, Response
from wsgiref.simple_server import make_server


app = Fleshl()

@app.add_route('/')
def index():
	response = Response(template="index.html", arg=app.request.query)
	return response
	
@app.add_route('/form')
def form():	
	if 'arg' not in app.request.post_data:
		readback = "Give some data!"
	elif app.request.post_data['arg']:
		readback = app.request.post_data['arg'][0]
	else:
		readback = "No information"
	
	response = Response(template="form.html", arg=readback)
	return response

@app.add_route('/favicon.ico')
def favicon():
	return Response(content=open('favicon.ico').read(), content_type="image/x-icon")

if __name__ == "__main__":
	httpd = make_server('localhost', 5000, app.run)
	httpd.serve_forever()