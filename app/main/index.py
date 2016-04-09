#-*- coding: UTF-8 -*-
from flask import Flask, render_template, redirect, request, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from get_tags import get_tags
from bookdata import get_bookinfo
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordRestRequestForm, PasswordResetForm, ChangeEmailForm
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from _email import send_email, mail
from config import Config
from models import User


app = Flask(__name__)
app.config = Config.init_app(app.config)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

mail.init_app(app)

# Things about User
'''@app.before_app_request
def berfore_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('unconfirmed'))'''


@login_manager.user_loader
def load_user(id):
    return User.query({'id': id})


@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('index'))
    return render_template('/unconfirmed.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query({'email': form.email.data})
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        User.commit(user.data)
        token = user.generate_confirmation_token()
        print token
        send_email(user.email, 'Confirm your Account', 'auth/email/confirm',
                   user=user, token=token)
        flash('A confirmation email has been sent to you')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))


@app.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your account', 'auth/email/confirm',
               user=current_user, token=token)
    flash('A new confirmation email has been sent to you!')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/music')
def musictags():
    tags = get_tags('music')
    if tags != []:
        return render_template('music.html', current_time=datetime.utcnow(), tags=tags, flag=0)
    else:
        return render_template('index.html', current_time=datetime.utcnow())


@app.route('/movie')
def movietags():
    tags = get_tags('movie')
    if tags != []:
        return render_template('movie.html', current_time=datetime.utcnow(), tags=tags, flag=0)
    else:
        return render_template('index.html', current_time=datetime.utcnow())


@app.route('/book')
def booktags():
    tags = get_tags('book')
    if tags != []:
        return render_template('book.html', current_time=datetime.utcnow(), tags=tags, flag=0)
    else:
        return render_template('index.html', current_time=datetime.utcnow())


@app.route('/bookinfo/<booktag>')
def bookinfo(booktag):
    page = request.args.get('page', 1, type=int)
    bookdata = get_bookinfo(booktag, page)
    print booktag
    if bookdata:
        print booktag
        return render_template('bookinfo.html', bookdata=bookdata, flag=0,booktag=booktag)
    else:
        return render_template('index.html', current_time=datetime.utcnow())


if __name__ == '__main__':
    manager.run()
