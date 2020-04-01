import unittest

from trackerApp import app
from trackerApp.models import User, Project, ProjectComment
from trackerApp.tests.BaseTest import BaseTest

class CommentViewTests(BaseTest):

    def add_project_comment(self, project_title, comment):
        # need a logged in user and a created project for this to work
        return self.app.post("/add_project_note/"+project_title, data=dict(
            comment=comment), follow_redirects=True)

    def test_add_project_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        # not logged in user should be redirected to login page
        response = self.add_project_comment("test_project", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to add item page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/add_project_note/test_project", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to add a note to the project test_project',
            response.data)
        # logged in user should land on task page with item now in list
        response = self.add_project_comment("test_project", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'test_project', response.data)
        self.assertIn(b'A test note', response.data)
