from fleshl import Fleshl, Response, spin_server


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

@app.add_route('/game')
def game():
	db = app.db_client[__name__]
	bubble_game = db.bubble_game	
	users = bubble_game.users
	if not users.find_one({'name':'Player'}):
		new_user = {'name':'Player', 'score': 1000}
		users.insert(new_user)
	user = users.find_one({'name':'Player'})
	user['score'] += 1
	users.save(user)
	response = Response(template="game.html", score=str(user['score']))
	return response

if __name__ == "__main__":
	httpd = spin_server('localhost', 5000, app.run)
	httpd.serve_forever()