from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import dbInterface
# imports to use Oauth2.0 as a way of login in with G+ and facebook
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials
import httplib2
import urllib2
import json
from flask import make_response
import requests

# globals
CLIENT_ID = json.loads(open('client_secret.json','r').read())['web']['client_id']
CATEGORYS = ["Soccer","Basketball","Baseball","Frisbee","Snowboarding",\
	"Rock Climbing","Skate","Hockey"] # All the itens categorys

app = Flask(__name__)


# Utility functions
def categorysToURL(categorys):  # Returns an array of category's name in a URL form
	return [[c, urllib2.quote(c)] for c in categorys]


# Route
@app.route('/')
def showItems():
	'''
		This function loads the application's main screen.
		First it generates the session state, then check if the user is logged
		to load ir properly, then it loads the itens from the database and
		finally it loads the screen template.
	''' 
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state

	if login_session.get('email'):
		user = dbInterface.getUserByEmail(login_session['email'])
	else:
		user = False

	items = dbInterface.getItems()

	return render_template('main.html', STATE=state, user=user,\
	 items=items, category=False, categorys=categorysToURL(CATEGORYS))

@app.route('/category', methods=['GET'])
def showCategory():
	'''
		This function loads the application's main screen, but it only loads
		the intens in the selected category.
		First it checks if the session state is correct and if the user is
		logged, then it loads the category's itens from the database and
		finally it loads the main screen template.
	''' 
	if request.args.get('state') == login_session['state']:# check if the state is correct
		user = dbInterface.getUserByEmail(login_session['email']) if\
		 login_session.get('email') else False
		state = login_session['state']
		category = request.args.get('category')
		items = dbInterface.getItemsByCategory(category)

		return render_template('main.html', STATE=state, user=user,\
		 items=items, category=category, categorys=categorysToURL(CATEGORYS))
	else:
		flash('Wrong state.')
		response = make_response(json.dumps("Wrong state."), 401)
		return response

@app.route('/item/new', methods=['POST'])
def newItem():
	'''
		This function saves a new item on the database
		First it checks if the state is correct, the user is logged and if all
		all mandatory info was inputed, then it saves the new item on the DB

	'''
	if request.args.get('state') == login_session['state']:# check if the state is correct
		if login_session.get('email'):# check if a user is logged
			user = dbInterface.getUserByEmail(login_session['email'])# get the user
			form = json.loads(request.data)# get the form with the item info 
			if form['name'] != '' and form['category'] in CATEGORYS:
				dbInterface.newItem(title=form['name'], category=form['category'],\
				 description=form['description'], user_id=user['id'])# save new item on DB
				flash('new item created.')
				response = make_response(json.dumps("New item created."), 200)
			else:
				flash("The itemn's name and category are mandatory.")
				response = make_response(json.dumps(\
					"The itemn's name and category are mandatory."), 401)
			return response
		else:
			flash('A user must be logged to add a new item.')
			response = make_response(json.dumps(\
				"A user must be logged to add a new item."), 401)
			return response
	else:
		flash('Wrong state.')
		response = make_response(json.dumps("Wrong state."), 401)
		return response

@app.route('/item/edit', methods=['POST'])
def editItem():
	'''
		This function edit a existing item on the database
		First it checks if the state is correct, the user is logged and if all
		all mandatory info was inputed, then it saves the edited item on the DB

	'''
	if request.args.get('state') == login_session['state']:# check if the state is correct
		if login_session.get('email'):# check if a user is logged
			user = dbInterface.getUserByEmail(login_session['email'])# get the user
			form = json.loads(request.data)# get the form with the item info
			#Check if the user is editing his item
			if str(user['id']) == str(form['userId']):
				# Check the mandatory information
				if form['name'] != '' and form['category'] in CATEGORYS:
					dbInterface.editItem(item_id=form['id'],title=form['name'],\
					 category=form['category'], description=form['description'],\
					 user_id=user['id'])# Save the edited item
					flash('Item edited.')
					response = make_response(json.dumps("Item edited."), 200)
				else:
					flash("The itemn's name and category are mandatory.")
					response = make_response(json.dumps(\
						"The itemn's name and category are mandatory."), 401)
			else:
				flash("The item can only be edited by the user who created it.")
				response = make_response(json.dumps(\
					"The item can only be edited by the user who created it."), 401)
			return response
		else:
			flash('A user must be logged to edit a item.')
			response = make_response(json.dumps(\
				"A user must be logged to edit a item."), 401)
			return response
	else:
		flash('Wrong state.')
		response = make_response(json.dumps("Wrong state."), 401)
		return response

@app.route('/item/delete', methods=['POST'])
def deleteItem():
	'''
		This function delete a existing item on the database
		First it checks if the state is correct, the user is logged
		then the item is deleted on the DB

	'''
	if request.args.get('state') == login_session['state']:# check if the state is correct
		if login_session.get('email'):# check if a user is logged
			user = dbInterface.getUserByEmail(login_session['email'])# get the user
			form = json.loads(request.data)# get the form with the item info 
			#Check if the user is deleting his item
			if str(user['id']) == str(form['userId']):
				dbInterface.deleteItem(item_id=form['id'])
				flash('Item deleted.')
				response = make_response(json.dumps("Item deleted."), 200)
			else:
				flash("The item can only be deleted by the user who created it.")
				response = make_response(json.dumps(\
					"The item can only be deleted by the user who created it."), 401)
			return response
		else:
			flash('A user must be logged to delete a item.')
			response = make_response(json.dumps(\
				"A user must be logged to delete a item."), 401)
			return response
	else:
		flash('Wrong state.')
		response = make_response(json.dumps("Wrong state."), 401)
		return response

# Making an API Endpoint (GET Request)
@app.route('/catalog.json', methods=['GET'])
def restaurantsJSON():
	'''
		This returns a json object of a dictionary containig all the itens
		on the DB

	'''
	return jsonify(Items=dbInterface.getItems());

# LOGIN
# to check if a user is logged in we can do de folowing on the pages that only logged in users can access
# if 'username' not in login_session:
# 	return redirect('/login')

# GPlus login
@app.route('/gconnect', methods=['POST'])
def gconnect():
	# check if is the same state
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# if the state is ok
	code = request.data
	try:
		# Upgrade autorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secret.json',scope="")
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the autorization code.', 401))
		response.headers['Content-Type'] = 'application/json'
		return response
	# Check that the access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')),500)
		response.headers['Content-Type'] = 'application/json'
		return response
	# verify that the access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		# response['Content-Type'] = 'application/json'
		return response
	# verify that the access token valid for this app
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID doesn't match app's."), 401)
		print "Token's client ID doesn't match app's."
		# response['Content-Type'] = 'application/json'
		return response
	# check to see if the user is alredy loged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps("Current user alredy connected."), 200)
		# response['Content-Type'] = 'application/json'
		return response
	# If none of the later if statements are true I can log in the user
	# Store the access token in the session for later use
	login_session['credentials'] = credentials.to_json()
	login_session['gplus_id'] = gplus_id
	# get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params = params)
	data = json.loads(answer.text)

	login_session['provider'] = 'google'
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# check if the user does not exist in the DB, if dont create a new user
	user = dbInterface.getUserByEmail(login_session['email'])
	if not user:
		user = dbInterface.newUser(login_session['username'], login_session['email'], 'None')

	login_session['user_id'] = user['id']

	output = ''
	output += '<h1>Wellcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += '" style = "width:300px; height:300px;border-radius:150px;"> '
	flash('You are now loged in as %s'%login_session['username'])
	return output

# GPlus LOG OUT
@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a user
	credentials = Credentials().new_from_json(login_session.get('credentials'))
	if credentials is None:
		response = make_response(json.dumps("Current user not connected."), 401)
		# response['Content-Type'] = 'application/json'
		return response
	# Execute HTTP GET to revoke current token.
	access_token = credentials.access_token
	url = "https://accounts.google.com/o/oauth2/revoke?token=%s"%access_token
	h = httplib2.Http()
	result = h.request(url,'GET')[0]

# FB Login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
	print 'Connecting via FACEBOOK'
	# check if is the same state
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# if the state is ok
	access_token = request.data
	# Exchange client token for long-lived server-side token
	fb_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']
	url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" %(fb_secret['app_id'],fb_secret['app_secret'],access_token)
	h = httplib2.Http()
	result =  h.request(url,'GET')[1]

	# Use token to get user info from API
	userinfo_url = "https://graph.facebook.com/v2.2/me"
	# strip expire tag from access token
	token = result.split('&')[0]

	url = 'https://graph.facebook.com/v2.2/me?%s' %token
	h = httplib2.Http()
	result =  h.request(url,'GET')[1]
	data = json.loads(result)

	login_session['provider'] = 'facebook'
	login_session['username'] = data['name']
	login_session['facebook_id'] = data['id']
	login_session['email'] = data['email']

	# Get users picture
	url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200'%token
	h = httplib2.Http()
	result =  h.request(url,'GET')[1]
	data = json.loads(result)

	login_session['picture'] = data['data']['url']

	# check if the user does not exist in the DB, if dont create a new user
	user = dbInterface.getUserByEmail(login_session['email'])
	if not user:
		user = dbInterface.newUser(login_session['username'], login_session['email'], 'None')

	login_session['user_id'] = user['id']

	output = ''
	output += '<h1>Wellcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += '" style = "width:300px; height:300px;border-radius:150px;"> '
	flash('You are now loged in as %s'%login_session['username'])
	return output

# FB LOG OUT
@app.route('/fbdisconnect')
def fbdisconnect():
	# Execute HTTP GET to revoke current token.
	facebook_id = login_session['facebook_id']
	url = "https://graph.facebook.com/%s/permissions"%facebook_id
	h = httplib2.Http()
	result = h.request(url,'DELETE')[1]

@app.route('/disconnect')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
			gdisconnect()
			del login_session['gplus_id']
			del login_session['credentials']
		if login_session['provider'] == 'facebook':
			fbdisconnect()
			del login_session['facebook_id']

		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		flash('You have successfully been logged out.')
		return redirect(url_for('showItems'))

	else:
		flash('You are not logged in.')
		return redirect(url_for('showItems'))

if __name__ == '__main__':
	app.secret_key = 'Chave_mto_S3C43T@-D0*C@L!xT0.'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
