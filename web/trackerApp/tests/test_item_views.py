import unittest

from trackerApp import app
from trackerApp.models import User, Project, Task, Item
from trackerApp.tests.BaseTest import BaseTest

class ItemViewTests(BaseTest):

    def add_item(self, task_title, item_title, description):
        # need a logged in user, a created project, and a created task for this to work
        return self.app.post("/add_item/"+task_title, data=dict(title=item_title,
            description=description), follow_redirects=True)

    def test_add_item(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Task Test", 1, 1)
        # not logged in user should be redirected to login page
        response = self.add_item("test_task", "test_item", "Item Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to add item page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/add_item/test_task", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to add an item to the task test_task',
            response.data)
        # logged in user should land on task page with item now in list
        response = self.add_item("test_task", "test_item", "Item Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Overview', response.data)
        self.assertIn(b'test_task', response.data)
        self.assertIn(b'test_item', response.data)
