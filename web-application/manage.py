#!/usr/bin/env python
import os
from flask_script import Manager

from main import config
from main.app import App
from frontend.views import frontend
from flask_migrate import MigrateCommand


def app_factory(conf, app_name):
    app = App(app_name)
    app.configure(conf)
    app.secret_key = os.urandom(24)
    app.add_blueprint_list((frontend,))
    app.setup()
    return app


if __name__ == '__main__':
    manager = Manager(app_factory)
    manager.add_command('db', MigrateCommand)
    manager.add_option("-n", "--name", dest="app_name", required=False, default=config.Config.PROJECT)
    manager.add_option("-c", "--config", dest="conf", required=False, default=config.DevelopConfig)
    manager.run()
