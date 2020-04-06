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

    def update_project(self, project_id, title, description):
        project = Project.query.filter_by(project_id=project_id).first()
        return self.app.post("/project/"+project.title+"/update", follow_redirects=True,
            data=dict(title=title, description=description))

    def delete_project(self, title):
        return self.app.get("/project/"+title+"/delete", follow_redirects=True)

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
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'test_project', response.data)
        # home page should have project name on it now
        response = self.app.get("/home", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_project', response.data)


    def test_update_project(self):
        self.create_user(user_name="testuser", email="test@test.com", password="testpass")
        self.create_project("test_project", "Project Test", 1)
        # not logged in user should be redirected to login page
        response = self.update_project(1, "test_UPDATE_project", "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user GET should land on update project page
        response = self.login_user("test@test.com", "testpass")
        response = self.app.get("/project/test_project/update", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update this Project', response.data)
        self.assertIn(b'test_project', response.data)
        self.assertIn(b'Project Test', response.data)
        # logged in user POST should land on project overview
        response = self.update_project(1, "test_UPDATE_project", "A test update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Overview', response.data)
        self.assertIn(b'test_UPDATE_project', response.data)
        self.assertIn(b'A test update', response.data)

    def test_delete_project(self):
        self.create_user("testuser", "test@test.com", "testpass")
        self.create_project("test_project", "Project Test", 1)
        # not logged in user should be redirected to login page
        response = self.delete_project("test_project")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        # logged in user should delete project and land on home page
        response = self.login_user("test@test.com", "testpass")
        response = self.delete_project("test_project")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'test_project', response.data)
