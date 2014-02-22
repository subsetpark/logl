from logl import Logl, Response, spin_server


app = Logl()

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

@app.add_route('/bettergame')
def better_game():
	db = app.db_client[__name__]
	zelda = db.zelda
	users = zelda.users
	name_choice = ""
	score = 0
	user = {}
	
	if 'POST' in app.request.method:
		if 'username' in app.request.post_data:
			name_choice = app.request.post_data['username'][0]
		else:
			name_choice = ''
	elif 'GET' in app.request.method:
		if 'username' in app.request.q_strings:
			name_choice = app.request.q_strings['username'][0]
		else:
			name_choice = ''

	if name_choice is not '':
		if not users.find_one({'name': name_choice}):
			new_user = {'name' : name_choice, 'score': 1000}
			users.insert(new_user)
		user = users.find_one({'name' : name_choice})
		user['score'] += 1
		users.save(user)

		score = user['score']
	response = Response(template="bettergame.html", username=name_choice, score=str(score))
	return response

if __name__ == "__main__":
	httpd = spin_server('localhost', 5000, app.run)
	httpd.serve_forever()