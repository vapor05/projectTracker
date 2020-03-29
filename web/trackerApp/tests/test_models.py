import unittest

from trackerApp import app, db
from trackerApp.models import User, Project
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

        project = Project.find_by_title("test_project")
        self.assertEquals(project.project_id, 1)
        self.assertEquals(project.description, "A test project")
