from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
                    ValidationError)
from wtforms.validators import Required, Regexp, Length, Email, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField('Email or Username', validators=[Required(), 
                                             Length(1, 64)])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), 
                                             Length(1, 64), 
                                             Email()])
    username = StringField('Username', validators=[
            Required(),
            Length(1, 64),
            Regexp(r'^[a-zA-Z][a-zA-Z_.]*$', 0, 'Username must only contain '
            'numbers, letters, dots or underscores.')])
    password = PasswordField('Password', validators=[Required(),
            EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

