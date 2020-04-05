import unittest

from trackerApp import app
from trackerApp.models import User, Project, Task, Item
from trackerApp.tests.BaseTest import BaseTest

class ItemViewTests(BaseTest):

    def add_item(self, task_title, item_title, description):
        # need a logged in user, a created project, and a created task for this to work
        return self.app.post("/add_item/"+task_title, data=dict(title=item_title,
            description=description), follow_redirects=True)

    def update_item(self, item_id, title, description):
        item = Item.query.filter_by(item_id=item_id).first()
        return self.app.post("/item/"+item.title+"/update", data=dict(title=title,
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
        # logged in user should land on overview page for new item
        response = self.add_item("test_task", "test_item", "Item Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item Overview', response.data)
        self.assertIn(b'test_item', response.data)
        self.assertIn(b'Item Test', response.data)
        # task overview page should have this new item in item list
        response = self.app.get("/task_overview/test_task", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_item', response.data)

    def test_update_item(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Task Test", 1, 1)
        self.create_item("test_item", "Item Test", 1, 1)
        # not logged in user should be redirected to login page
        response = self.update_item(1, "test_UPDATE_item", "Item UPDATE Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to update item page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/item/test_item/update", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update this Item', response.data)
        # logged in user should land on overview page for updated item
        response = self.update_item(1, "test_UPDATE_item", "Item UPDATE Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item Overview', response.data)
        self.assertIn(b'test_UPDATE_item', response.data)
        self.assertIn(b'Item UPDATE Test', response.data)
