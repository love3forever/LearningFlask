#-*- coding: UTF-8 -*- 
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bleach
from flask import current_app,request
from flask.ext.login import UserMixin,AnonymousUserMixin
from db import client


class User(UserMixin):
	def __init__(self,email,username,password,location,about_me):
		self.email=email
		self.username = username
		self.password = password
		self.confirmed = False
		self.location = location
		self.about_me = about_me
		self.client = client
		self.col = client['flask']['users']
		self.data = {
					"email":self.email,
					"username":self.username,
					"password":password,
					"confirmed":self.confirmed,
					"location":self.location,
					"about_me":self.about_me
			}

	@staticmethod
	def query(data):
		col = client['flask']['users']
		cursor = col.find(data).limit(1)
		for doc in cursor:
			u =User(email=doc['email'],
                     username=doc['username'],
                     password=doc['password'],
                     location=doc['location'],
                     about_me=doc['about_me']
                     )
			return u 
	@staticmethod
	def generate_fake(count=100):
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			u =User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence())
			data = u.data
			
			u.col.insert_one(data)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self,password):
		self.password_hash= generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def generate_confirmation_token(self,expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm':self.id})

	def confirm(self,token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm')!=self.id:
			return False
		self.confirm = True
		self.col.update_one(
			{'email',self.email},
			{"$set":{"confirmed":self.confirmed}}
			)
		return True

	def generate_reset_token(self,expiration=3600):
		s =Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'reset':self.id})

	def reset_password(self,token,new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except :
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		self.col.update_one(
			{'email',self.email},
			{"$set":{"password":self.password}}
			)
		return True


User.generate_fake(100)

print User.query({'username':'martha65'}).email

