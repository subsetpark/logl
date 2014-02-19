from fleshl import Fleshl
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

app = Fleshl()

@app.add_route('/')
def index():
	return "There's nothing here!"
	
httpd = make_server('localhost', 5000, app.run)
httpd.serve_forever()