from tests.base import BaseTestCase


class TestBroView(BaseTestCase):
    def test_signin_view(self):
        response = self.client.get('/signin')
        self.assertIn("Sign In  | Bro", response.data.decode('utf-8'))

    def test_signup_view(self):
        response = self.client.get('/signup')
        self.assertIn("Sign Up  | Bro", response.data.decode('utf-8'))

    def test_signout_view(self):
        response = self.client.get('/signout')
        self.assertNotIn("404 Not Found", response.data.decode('utf-8'))

    def test_list_bros_view(self):
        response = self.client.get('/bros')
        self.assertIn("List Bros  | Bro", response.data.decode('utf-8'))

    def test_bro_profile_view(self):
        response = self.client.get('/bros/1')
        self.assertIn("great@test.com", response.data.decode('utf-8'))
