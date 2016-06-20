# -*- coding:utf-8 -*-
import os
from base import Base
from bro.models import AnonymousBro
from main.extensions import db, migrate, csrf_protect, login_manager
from frontend.views import frontend
from bro.views import bro
from main.settings import config


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


def app_factory(environment, app_name):
    app = App(app_name)
    app.configure(config=config[environment])
    app.secret_key = os.urandom(24)
    app.add_blueprint_list((frontend, bro,))
    app.setup()
    return app
