import unittest

from trackerApp import app
from trackerApp.models import User, Project, Task
from trackerApp.tests.BaseTest import BaseTest

class TaskViewTests(BaseTest, unittest.TestCase):

    def add_task(self, project_title, task_title, description):
        # need a logged in user and a created project for this to work
        return self.app.post("/add_task/"+project_title, data=dict(title=task_title,
            description=description), follow_redirects=True)

    def test_add_task(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        # not logged in user should be redirected to login page
        response = self.add_task("test_project", "test_task", "Task Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to start task page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/add_task/test_project", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to add a task to the project test_project',
            response.data)
        # logged in user should land on home page with project now in list
        response = self.add_task("test_project", "test_task", "Task Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'test_project', response.data)
        self.assertIn(b'test_task', response.data)
