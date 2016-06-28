from datetime import datetime, date

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from main.extensions import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

BCRYPT_LOG_ROUNDS = 12


@login_manager.user_loader
def get_user(bro_id):
    return Bro.query.get(int(bro_id))


class AnonymousBro(AnonymousUserMixin):
    def __init__(self):
        self.id = 0


friendship = db.Table('friendships', db.Model.metadata,
                      db.Column('bro_id', db.Integer, db.ForeignKey('bros.id', ondelete='cascade')),
                      db.Column('friend_id', db.Integer, db.ForeignKey('bros.id', ondelete='cascade')),
                      db.UniqueConstraint('bro_id', 'friend_id', name='unique_friendships'))


class Bro(db.Model, UserMixin):
    __tablename__ = "bros"

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(60), index=True)
    email = db.Column('email', db.String(255), unique=True, index=True)
    _password = db.Column('password', db.String(255))
    registered_on = db.Column('registered_on', db.DateTime, default=datetime.utcnow())
    birthdate = db.Column('birthday', db.DateTime)
    active = db.Column('is_active', db.Boolean, default=True)
    best_friend_id = db.Column(db.Integer, db.ForeignKey('bros.id', ondelete='SET NULL'))
    best_friend = relationship('Bro',
                               uselist=False,
                               remote_side=[id],
                               post_update=True
                               )

    friends = relationship('Bro', secondary=friendship,
                           primaryjoin=id == friendship.c.bro_id,
                           secondaryjoin=id == friendship.c.friend_id)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = generate_password_hash(plaintext, BCRYPT_LOG_ROUNDS)

    def is_active(self):
        return self.active

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<Bro username=%s>" % self.username

    def get_id(self):
        return unicode(self.id)

    def is_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    @property
    def age(self):
        today = date.today()
        born = self.birthdate
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def befriend(self, bro):
        if not self.is_same_bro(bro) and bro not in self.friends:
            self.friends.append(bro)
            bro.friends.append(self)

    def unfriend(self, bro):
        if not self.is_same_bro(bro) and bro in self.friends:
            self.friends.remove(bro)
            bro.friends.remove(self)

    def is_best_friend_with(self, bro):
        return self.best_friend == bro

    def add_best_friend(self, bro):
        if not self.is_best_friend_with(bro):
            self.best_friend = bro
            bro.best_friend = self

    def remove_best_friend(self, bro):
        if self.is_best_friend_with(bro):
            self.best_friend = None
            bro.best_friend = None

    def is_same_bro(self, bro):
        return self.id == bro.id

    def is_friend(self, bro):
        return True if bro.id in [friend.id for friend in self.friends] else False

    @property
    def friends_qty(self):
        return len(self.friends) + (1 if self.best_friend else 0)
