#-*- coding: UTF-8 -*- 
from flask import Flask,render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from get_tags import get_tags
from bookdata import get_bookinfo
from flask.ext.login import LoginManager
from models import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager.init_app(app)





@app.route('/')
def index():
	return render_template('index.html',current_time=datetime.utcnow())

@app.route('/music')
def musictags():
	tags = get_tags('music')
	if tags!=[]:
		return render_template('music.html',current_time=datetime.utcnow(),tags=tags,flag=0)
	else:
		return render_template('index.html',current_time=datetime.utcnow())

@app.route('/movie')
def movietags():
	tags = get_tags('movie')	
	if tags!=[]:
		return render_template('movie.html',current_time=datetime.utcnow(),tags=tags,flag=0)
	else:
		return render_template('index.html',current_time=datetime.utcnow())

@app.route('/book')
def booktags():
	tags = get_tags('book')	
	if tags!=[]:
		return render_template('book.html',current_time=datetime.utcnow(),tags=tags,flag=0)
	else:
		return render_template('index.html',current_time=datetime.utcnow())

@app.route('/bookinfo/<booktag>')
def bookinfo(booktag):
	bookdata = get_bookinfo(booktag)
	if bookdata:
		return render_template('bookinfo.html',bookdata=bookdata,flag=0)
	else:
		return render_template('index.html',current_time=datetime.utcnow())



if __name__ == '__main__':
	manager.run()