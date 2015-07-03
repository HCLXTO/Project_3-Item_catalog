import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
	# declare the table's name represented by this class
	__tablename__ = 'user'
	# declare the table's columns
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	email = Column(String(80), nullable=False)
	password = Column(String(80), nullable=True)

	@property
	def toDict(self):
		# "Returns object data in easily serializable format"
		return {
			'id': self.id,
			'name': self.name,
			'email': self.email,
			'password': self.password,
		}


class Item(Base):
	# declare the table's name represented by this class
	__tablename__ = 'item'
	# declare the table's columns
	id = Column(Integer, primary_key=True)
	title = Column(String(80), nullable=False)
	category = Column(String(250))
	description = Column(String(250))
	# the reference here must be the tablename not the class name
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def toDict(self):
		# "Returns object data in easily serializable format"
		return {
			'id': self.id,
			'title': self.title,
			'category': self.category,
			'description': self.description,
			'user_id': self.user_id,
		}

# ---End of the file---
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
