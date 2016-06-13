# -*- coding:utf-8 -*-
from base import Base
from bro.models import AnonymousBro
from main.extensions import db, migrate, csrf_protect, login_manager


class App(Base):
    def configure_database(self):
        db.app = self
        db.init_app(self)

    def configure_extensions(self):
        migrate.init_app(self, db)
        csrf_protect.init_app(self)

    def configure_login_manager(self):
        login_manager.init_app(self)
        login_manager.login_view = 'bro.signin'
        login_manager.anonymous_user = AnonymousBro
