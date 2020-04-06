import unittest

from trackerApp import app, db
from trackerApp.models import User, Project, Task, Item, ProjectComment, TaskComment, ItemComment
from trackerApp.tests.BaseTest import BaseTest

class ModelTests(BaseTest, unittest.TestCase):

    def test_user(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        self.create_user(user_name="testuser2", email="test2@test.com", password="testpass2")

        user = User.query.filter_by(user_name = "testuser").first()
        self.assertEqual(user.get_id(), 1)
        self.assertTrue(user.check_password("testpass"))
        self.assertFalse(user.check_password("wrongpass"))


    def test_project(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        user = User.query.filter_by(user_name = "testuser").first()
        self.create_project(title="test_project", description="A test project", user_id=user.get_id())
        self.create_project(title="test_project2", description="Another test project", user_id=user.get_id())

        project = Project.find_by_title("test_project", 1)
        self.assertEquals(project.project_id, 1)
        self.assertEquals(project.description, "A test project")
        self.assertEquals(project.status_id, 1)

    def test_task(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        self.create_project(title="test_project", description="A test project",
            user_id=1)
        self.create_task(title="test_task", description="A test task", project_id=1,
            user_id=1)

        task = Task.find_by_title("test_task", 1)
        self.assertEquals(task.task_id, 1)
        self.assertEquals(task.description, "A test task")
        self.assertEquals(task.status_id, 1)

    def test_project_delete(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        self.create_project(title="test_project", description="A test project", user_id=1)
        self.create_comment("project", "test note", 1, 1)
        project = Project.query.filter_by(project_id=1).first()
        project.delete()
        self.assertTrue(not Project.query.filter_by(project_id=1).first())
        self.assertTrue(not ProjectComment.query.filter_by(project_comment_id=1).first())

    def test_task_delete(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        self.create_project(title="test_project", description="A test project", user_id=1)
        self.create_task(title="test_task", description="A test task", project_id=1,
            user_id=1)
        self.create_comment("task", "test note", 1, 1)
        task = Task.query.filter_by(task_id=1).first()
        task.delete()
        self.assertTrue(not Task.query.filter_by(task_id=1).first())
        self.assertTrue(not TaskComment.query.filter_by(task_comment_id=1).first())

    def test_item_delete(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        self.create_project(title="test_project", description="A test project", user_id=1)
        self.create_task(title="test_task", description="A test task", project_id=1,
            user_id=1)
        self.create_item("test_item", "Test Task", 1, 1)
        self.create_comment("item", "Test Note", 1, 1)
        item = Item.query.filter_by(item_id=1).first()
        item.delete()
        self.assertTrue(not Item.query.filter_by(item_id=1).first())
        self.assertTrue(not ItemComment.query.filter_by(item_comment_id=1).first())
