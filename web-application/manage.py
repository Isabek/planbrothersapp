#!/usr/bin/env python
import os
from flask_script import Manager, Server

from main.settings import config
from main.app import App
from frontend.views import frontend
from flask_migrate import MigrateCommand
from bro.views import bro


def app_factory(environment, app_name):
    app = App(app_name)
    app.configure(config=config[environment])
    app.secret_key = os.urandom(24)
    app.add_blueprint_list((frontend, bro,))
    app.setup()
    return app


if __name__ == '__main__':
    manager = Manager(app_factory)
    manager.add_command('db', MigrateCommand)
    manager.add_command('runserver', Server(host='0.0.0.0'))
    manager.add_option("-n", "--name", dest="app_name", required=False, default='default')
    manager.add_option("-e", "--environment", dest="environment", required=False, default='development')
    manager.run()
