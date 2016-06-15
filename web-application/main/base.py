# -*- coding:utf-8 -*-
from flask import Flask, render_template


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
        self.configure_login_manager()

    def configure_error_handlers(app):
        @app.errorhandler(404)
        def page_not_found(error):
            return render_template('error/404.html'), 404

        @app.errorhandler(500)
        def page_not_found(error):
            return render_template('error/500.html'), 500

    def configure_database(self):
        pass

    def configure_extensions(self):
        pass

    def configure_login_manager(self):
        pass
