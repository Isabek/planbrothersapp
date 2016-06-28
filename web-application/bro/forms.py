from bro.models import Bro
from flask_wtf import Form
from wtforms import PasswordField, StringField, DateField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo


class SignInForm(Form):
    email = StringField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    remember = BooleanField('Remember me?')


class SignUpForm(Form):
    username = StringField('Username', [DataRequired()])
    email = StringField('Email', [Email()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])
    birthdate = DateField('Birth Date', [InputRequired()], format='%m/%d/%Y')

    def validate_for_exist(self, current_bro=None):
        rv = Form.validate(self)
        if not rv:
            return False

        if not current_bro and self._get_bro_by_email(self.email.data):
            self.email.errors.append("Bro with this email exists")
            return False

        bro = self._get_bro_by_email(self.email.data)
        if bro and current_bro and bro.get_id() != current_bro.get_id():
            self.email.errors.append("Bro with this email exists")
            return False
        return True

    @staticmethod
    def _get_bro_by_email(email):
        return Bro.query.filter_by(email=email).first()


class DeleteForm(Form):
    pass
