from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError


class LoginForm(Form):
	email = StringField('Email',validators=[Reqiured(),Length(1,64),Email()])
	password = PasswordField('Password',validators=[Reqiured()])
	remember_me = BooleanField('Keep me logged in.')
	submit = SubmitField('Login In')

class RegistrationForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self,field):
    	
