import unittest

from trackerApp import app
from trackerApp.models import User, Project, ProjectComment, TaskComment, ItemComment
from trackerApp.tests.BaseTest import BaseTest

class CommentViewTests(BaseTest):

    def add_project_comment(self, project_title, comment):
        # need a logged in user and a created project for this to work
        return self.app.post("/add_project_note/"+project_title, data=dict(
            comment=comment), follow_redirects=True)

    def add_task_comment(self, task_title, comment):
        # need a logged in user, a created project, and a create task for this to work
        return self.app.post("/add_task_note/"+task_title, data=dict(
            comment=comment), follow_redirects=True)

    def add_item_comment(self, item_title, comment):
        # need a logged in user, a created project, and a create task for this to work
        return self.app.post("/add_item_note/"+item_title, data=dict(
            comment=comment), follow_redirects=True)

    def update_comment(self, url, id, comment):
        return self.app.post(url+"/"+str(id)+"/update", data=dict(comment=comment),
            follow_redirects=True)

    def test_add_project_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        # not logged in user should be redirected to login page
        response = self.add_project_comment("test_project", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to add note page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/add_project_note/test_project", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to add a note to test_project',
            response.data)
        # logged in user should land on project page with note now in list
        response = self.add_project_comment("test_project", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'test_project', response.data)
        self.assertIn(b'A test note', response.data)

    def test_update_project_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_comment("project", "A test note", 1, 1)
        # not logged in user should be redirected to login page
        response = self.update_comment("/project_note", 1, "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # get on update page should have old comment on page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/project_note/1/update", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update this Note', response.data)
        self.assertIn(b'A test note', response.data)
        # logged in user should go to project page with updated note in list
        response = self.update_comment("/project_note", 1, "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'A test update', response.data)

    def test_add_task_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Test Task", 1, 1)
        # not logged in user should be redirected to login page
        response = self.add_task_comment("test_task", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to add note page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/add_task_note/test_task", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to add a note to test_task',
            response.data)
        # logged in user should land on task page with note now in list
        response = self.add_task_comment("test_task", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Overview', response.data)
        self.assertIn(b'test_task', response.data)
        self.assertIn(b'A test note', response.data)

    def test_update_task_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Test Task", 1, 1)
        self.create_comment("task", "A test note", 1, 1)
        # not logged in user should be redirected to login page
        response = self.update_comment("/task_note", 1, "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # get on update page should have old comment on page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/task_note/1/update", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update this Note', response.data)
        self.assertIn(b'A test note', response.data)
        # logged in user should go to project page with updated note in list
        response = self.update_comment("/task_note", 1, "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Overview', response.data)
        self.assertIn(b'A test update', response.data)

    def test_add_item_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Test Task", 1, 1)
        self.create_item("test_item", "Test Item", 1, 1)
        # not logged in user should be redirected to login page
        response = self.add_item_comment("test_item", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should get to add note page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/add_item_note/test_item", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fill in the below form to add a note to test_item',
            response.data)
        # logged in user should land on item page with note now in list
        response = self.add_item_comment("test_item", "A test note")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item Overview', response.data)
        self.assertIn(b'test_item', response.data)
        self.assertIn(b'A test note', response.data)

    def test_update_item_comment(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        self.create_task("test_task", "Test Task", 1, 1)
        self.create_item("test_item", "Test Item", 1, 1)
        self.create_comment("item", "A test note", 1, 1)
        # not logged in user should be redirected to login page
        response = self.update_comment("/item_note", 1, "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # get on update page should have old comment on page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/item_note/1/update", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update this Note', response.data)
        self.assertIn(b'A test note', response.data)
        # logged in user should go to project page with updated note in list
        response = self.update_comment("/item_note", 1, "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item Overview', response.data)
        self.assertIn(b'A test update', response.data)
