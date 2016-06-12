# -*- coding:utf-8 -*-
from base import Base
from main.extensions import db, migrate


class App(Base):
    def configure_database(self):
        db.app = self
        db.init_app(self)

    def configure_extensions(self):
        migrate.init_app(self, db)
