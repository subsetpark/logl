from logl import Logl, Response

app = Logl()

@app.add_route('/')
def index():
	app.add_replace('query', app.request.query)
	response = app.response(template="index.html")
	return response
	
@app.add_route('/form')
def form():	
	if 'arg' not in app.request.post_data:	
		app.add_replace('data', "Give some data!")
	elif app.request.post_data['arg']:
		app.add_replace('data', app.request.post_data['arg'][0])
	
	response = app.response(template="form.html")
	return response

@app.add_route('/if')
def iff():
	app.add_con('first', False)
	app.add_con('second', False)

	if 'ifs' in app.request.post_data:
		if 'first' in app.request.post_data['ifs']:
			app.add_con('first', True)
		if 'second' in app.request.post_data['ifs']:
			app.add_con('second', True)
	print app.request.post_data

	response = app.response(template='if.html')
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
	app.add_replace('score', str(user['score']))
	
	response = app.response(template="game.html")
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

		app.add_replace('username', name_choice)
		app.add_replace('score', str(user['score']))
	response = app.response(template="bettergame.html")
	return response

if __name__ == "__main__":
	app.start('localhost', 5000)