import os
import unittest

from trackerApp import app, db
from trackerApp.models import User, Project

TEST_DB = 'test.db'

class BaseTest(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config['WTF_CSRF_ENABLED'] = False
        basedir = os.path.abspath(os.path.dirname(__file__))
        datadir = os.path.join(basedir, "testdata")

        if not os.path.exists(datadir):
            os.mkdir(datadir)

        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(datadir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def create_user(self, user_name, email, password):
        user = User(user_name = user_name, email=email, password=password)
        user.save_to_db()

    def create_project(self, title, description, user_id):
        project = Project(title=title, description=description, user_id=user_id)
        project.save_to_db()
