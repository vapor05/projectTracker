import os
import unittest

from trackerApp import app, db
from trackerApp.models import User, Project
from trackerApp.tests.BaseTest import BaseTest

class ProjectViewTests(BaseTest, unittest.TestCase):

    def start_project(self, title, description):
        # need a logged in user first for this to work
        return self.app.post("/create_project", data=dict(title=title,
            description=description), follow_redirects=True)

    def test_create_project(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        # not logged in user should be redirected to login page
        response = self.start_project("test_project", "A test project")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to start project page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/create_project", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to start a new Project', response.data)
        # logged in user should land on home page with project now in list
        response = self.start_project("test_project", "A test project")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home page for testuser', response.data)
        self.assertIn(b'test_project', response.data)
