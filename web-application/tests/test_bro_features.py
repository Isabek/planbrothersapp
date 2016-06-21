from tests.base import BaseTestCase


class TestBroFeatures(BaseTestCase):
    def login(self, email, password):
        return self.client.post('/signin', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def register(self, path, email, password, confirm, username, birthdate):
        return self.client.post(path, data=dict(
            email=email,
            password=password,
            confirm=confirm,
            username=username,
            birthdate=birthdate
        ), follow_redirects=True)

    def signup(self, email, password, confirm, username, birthdate):
        return self.register('/signup', email, password, confirm, username, birthdate)

    def edit(self, email, password, confirm, username, birthdate):
        return self.register('/profile/edit', email, password, confirm, username, birthdate)

    def logout(self):
        return self.client.get('/signout', follow_redirects=True)

    def test_bro_login(self):
        rv = self.login("great@test.com", "Great")
        assert "Bro logged in successfully" in rv.data.decode('utf-8')

    def test_bro_logout(self):
        self.login("great@test.com", "Great")
        rv = self.logout()
        assert "Bro logged out successfully" in rv.data.decode('utf-8')

    def test_bro_signup(self):
        rv = self.signup('pytest@mail.test', 'test', 'test', 'Py Test', '06/06/2006')
        assert "Bro has been successfully registered." in rv.data.decode('utf-8')

    def test_bro_edit_profile(self):
        self.signup('newton@mail.test', 'test', 'test', 'Isaac Newton', '04/01/1643')
        self.login('newton@mail.test', 'test')
        rv = self.edit('newton@mail.test', 'test', 'test', 'Giordano Bruno', '04/01/1643')

        assert 'You profile has been successfully updated.' in rv.data.decode('utf-8')
        assert 'Giordano Bruno' in rv.data.decode('utf-8')

    def test_bro_delete_profile(self):
        self.signup('galileo@mail.test', 'test', 'test', 'Galileo', '04/01/1643')
        self.login('galileo@mail.test', 'test')

        rv = self.client.post('/profile/delete', follow_redirects=True)
        assert "You profile has been successfully deleted" in rv.data.decode('utf-8')

    def test_friend_bro(self):
        self.login("great@test.com", "Great")
        rv = self.client.get('/bros/friend/%s' % 2, follow_redirects=True)

        assert "Bro has been successfully added as a friend" in rv.data.decode('utf-8')

    def test_unfriend_bro(self):
        self.login("great@test.com", "Great")
        rv = self.client.get('/bros/unfriend/%s' % 2, follow_redirects=True)

        assert "Bro has been successfully unfriended" in rv.data.decode('utf-8')

    def test_add_best_friend_bro(self):
        self.login("great@test.com", "Great")
        rv = self.client.get('/bros/best_friend/%s' % 2, follow_redirects=True)

        assert "Bro has been successfully added as a best friend" in rv.data.decode('utf-8')

    def test_remove_best_friend_bro(self):
        self.login("great@test.com", "Great")
        rv = self.client.get('/bros/remove_best_friend/%s' % 2, follow_redirects=True)

        assert "Best Bro has been successfully unfriended" in rv.data.decode('utf-8')
