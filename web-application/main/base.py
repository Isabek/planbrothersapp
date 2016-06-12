# -*- coding:utf-8 -*-
from flask import Flask


class Base(Flask):
    def configure(self, config):
        self.config.from_object(config)

    def add_blueprint(self, blueprint):
        self.register_blueprint(blueprint=blueprint)

    def add_blueprint_list(self, blueprints):
        for blueprint in blueprints:
            self.add_blueprint(blueprint)

    def setup(self):
        self.configure_error_handlers()
        self.configure_database()
        self.configure_extensions()

    def configure_error_handlers(self):
        pass

    def configure_database(self):
        pass

    def configure_extensions(self):
        pass
