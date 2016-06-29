import unittest

from flask_fixtures import FixturesMixin
from main.app import app_factory
from main.extensions import db


class BaseTestCase(unittest.TestCase, FixturesMixin):
    fixtures = ['bros.json']

    app = app_factory('test', 'Test')
    db = db

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)
