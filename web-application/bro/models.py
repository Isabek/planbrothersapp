from datetime import datetime, date

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from main.extensions import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property

BCRYPT_LOG_ROUNDS = 12


@login_manager.user_loader
def get_user(bro_id):
    return Bro.query.get(int(bro_id))


class Bro(db.Model, UserMixin):
    __tablename__ = "bros"

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(60), index=True)
    email = db.Column('email', db.String(255), unique=True, index=True)
    _password = db.Column('password', db.String(255))
    registered_on = db.Column('registered_on', db.DateTime)
    birthdate = db.Column('birthday', db.DateTime)
    active = db.Column('is_active', db.Boolean, default=True)

    def __init__(self, username, password, email, birthdate):
        self.username = username
        self.password = password
        self.email = email
        self.birthdate = birthdate
        self.registered_on = datetime.utcnow()

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = generate_password_hash(plaintext, BCRYPT_LOG_ROUNDS)

    def is_active(self):
        return self.active

    def __repr__(self):
        return self.username

    def get_id(self):
        return unicode(self.id)

    def is_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    @property
    def age(self):
        today = date.today()
        born = self.birthdate
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
