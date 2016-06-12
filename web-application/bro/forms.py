from flask_wtf import Form
from wtforms import PasswordField, StringField, DateField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo


class SignInForm(Form):
    email = StringField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    remember = BooleanField('Remember me?')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class SignUpForm(Form):
    username = StringField('Username', [DataRequired()])
    email = StringField('Email', [Email()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])
    birthdate = DateField('Birth Date', [InputRequired()], format='%m/%d/%Y')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
