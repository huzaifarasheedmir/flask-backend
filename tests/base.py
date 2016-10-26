from flask import current_app
from flask.ext.testing import TestCase

from app import create_app as create_test_app

TestCase.maxDiff = None


class BaseTestCase(TestCase):
    """A base test case"""

    def create_app(self):
        return create_test_app("testing")

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        pass

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
