#!/usr/bin/env python
import os
from commands.populate_bros import PopulateBrosCommand
from commands.run_tests import RunTestsCommand
from flask_script import Manager, Server

from application.main.app import app_factory
from flask_migrate import MigrateCommand

if __name__ == '__main__':
    manager = Manager(app_factory)
    manager.add_command('db', MigrateCommand)
    manager.add_command('populate_bros', PopulateBrosCommand)
    manager.add_command('test', RunTestsCommand)
    manager.add_command('runserver', Server(host='0.0.0.0', port=os.environ.get('PORT', 5000)))
    manager.add_option("-n", "--name", dest="app_name", required=False, default='default')
    manager.add_option("-e", "--environment", dest="environment", required=False, default='development')
    manager.run()
