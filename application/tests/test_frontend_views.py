from tests.base import BaseTestCase


class TestFrontendView(BaseTestCase):
    def test_home_view(self):
        response = self.client.get('/')
        self.assertIn("Welcome to the Bro Social Network.", response.data.decode('utf-8'))
