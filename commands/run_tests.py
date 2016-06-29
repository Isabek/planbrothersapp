import unittest

from flask_script import Command


class RunTestsCommand(Command):
    def run(self):
        test_loader = unittest.defaultTestLoader
        test_runner = unittest.TextTestRunner()
        test_suite = test_loader.discover('.')
        test_runner.run(test_suite)
