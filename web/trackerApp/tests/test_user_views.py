import os
import unittest

from trackerApp import app, db
from trackerApp.models import User
from trackerApp.tests.BaseTest import BaseTest

TEST_DB = 'usertest.db'

class UserViewTests(BaseTest, unittest.TestCase):

    def test_register(self):
        response = self.app.get("/register", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.register_user("testuser", "test@test.com", "testpass")
        self.assertEqual(response.status_code, 200)
        user = User.query.all()
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].user_name, "testuser")
        self.assertEqual(user[0].email, "test@test.com")

    def test_login(self):
        # test view is up
        response = self.app.get("/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # test login of non existing user
        response = self.login_user("test@test.com", "testpass")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # test bad login of existing user
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        response = self.login_user("test@test.com", "wrongpass")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # test login of existing user
        response = self.login_user("test@test.com", "testpass")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home page for testuser', response.data)

    def test_logout(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        response = self.login_user("test@test.com", "testpass")
        self.assertIn(b'Home page for testuser', response.data)
        response = self.logout_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Track Your Projects', response.data)

    def test_home_page(self):
        # test not logged in user is redirected to login
        response = self.app.get("/home", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In',response.data)
        # test logged in user goes to home page and sees projects
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        response = self.login_user("test@test.com", "testpass")
        self.assertIn(b'Home page for testuser', response.data)
        self.create_project(title="testproject", description="test description",
            user_id=1)
        response = self.login_user("test@test.com", "testpass")
        self.assertIn(b'testproject', response.data)

if __name__ == "__main__":
    unittest.main()
