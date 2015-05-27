from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Item

engine = create_engine('sqlite:///itemcatalog.db')#this tell what database we will refer
Base.metadata.bind = engine#makes the consections with our class definitions and their corresponding tables in the DB
DBSession = sessionmaker(bind = engine)#the session is used to pass commands to the database



def getUsers():
	session = DBSession()
	users = session.query(User).all()
	return [i.serialize for i in users]

def getUser(id):
	session = DBSession()
	try:
		user = session.query(User).filter_by(id=id).one()
		return user.serialize
	except:
		return False

def getUserByEmail(email):
	session = DBSession()
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.serialize
	except:
		return False

def editUser(id, name, email, password):
	session = DBSession()

	user = session.query(User).filter_by(id=id).one()
	user.name = name
	user.email = email
	user.password = password
	session.add(user)
	session.commit()

	return True

def deleteUser(id):
	session = DBSession()

	user = session.query(User).filter_by(id=id).one()
	session.delete(user)
	session.commit()

	return True

def newUser(name, email, password):
	session = DBSession()

	newUser = User(name = name, email=email, password=password)
	session.add(newUser)
	session.commit()

	return newUser.serialize

def getItems():
	session = DBSession()
	items = session.query(Item).all()
	return [i.serialize for i in items]

def getItemsByCategory(category):
	session = DBSession()
	items = session.query(Item).filter_by(category=category).all()
	return [i.serialize for i in items]

def getItem(item_id):
	session = DBSession()
	item = session.query(Item).filter_by(id=item_id).one()
	return item.serialize

def editItem(item_id, title, category, description, user_id):
	session = DBSession()

	item = session.query(Item).filter_by(id=item_id).one()
	item.title = title
	item.category = category
	item.description = description
	item.user_id = user_id

	session.add(item)
	session.commit()

	return True

def deleteItem(item_id):
	session = DBSession()

	item = session.query(Item).filter_by(id=item_id).one()
	session.delete(item)
	session.commit()
	return True

def newItem(title, category, description, user_id):
	session = DBSession()

	newItem = Item(title = title, category=category, description=description, user_id=user_id)
	session.add(newItem)
	session.commit()

	return True