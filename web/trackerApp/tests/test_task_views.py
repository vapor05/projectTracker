import unittest

from trackerApp import app
from trackerApp.models import User, Project, Task
from trackerApp.tests.BaseTest import BaseTest

class TaskViewTests(BaseTest, unittest.TestCase):

    def add_task(self, project_title, task_title, description):
        # need a logged in user and a created project for this to work
        return self.app.post("/add_task/"+project_title, data=dict(title=task_title,
            description=description), follow_redirects=True)

    def update_task(self, task_id, title, description):
        task = Task.query.filter_by(task_id=task_id).first()
        return self.app.post("task/"+task.title+"/update", data=dict(title=title,
            description=description), follow_redirects=True)

    def delete_task(self, title):
        return self.app.get("/task/"+title+"/delete", follow_redirects=True)

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
        # logged in user should land on task overview page
        response = self.add_task("test_project", "test_task", "Task Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Overview', response.data)
        self.assertIn(b'test_task', response.data)
        # task should be on project overview task list now
        response = self.app.get("/project_overview/test_project", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'test_project', response.data)
        self.assertIn(b'test_task', response.data)

    def test_update_task(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Test Task", 1, 1)
        # not logged in user should be redirected to login page
        response = self.update_task(1, "test_UPDATE_task", "Task Test UPDATE")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to update task page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/task/test_task/update", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update this Task', response.data)
        # logged in user should land on Overview page with updated task now in list
        response = self.update_task(1, "test_UPDATE_task", "Task Test UPDATE")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Overview', response.data)
        self.assertIn(b'test_UPDATE_task', response.data)
        self.assertIn(b'Task Test UPDATE', response.data)

    def test_delete_task(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Test Task", 1, 1)
        # not logged in user should be redirected to login page
        response = self.delete_task("test_task")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should delete project and land on home page
        response = self.login_user("test@test.com", "testpass")
        response = self.delete_task("test_task")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'test_task', response.data)
