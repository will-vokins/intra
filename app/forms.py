from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=6, max=128)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('passwordConfirm', message='Passwords must match!')
    ])
    passwordConfirm = PasswordField('Confirm Password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password')