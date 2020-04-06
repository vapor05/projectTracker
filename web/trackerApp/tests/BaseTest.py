import os
import unittest

from trackerApp import app, db
from trackerApp.models import User, Project, Task, Item, ProjectComment, TaskComment, ItemComment

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

    def create_task(self, title, description, project_id, user_id):
        task = Task(title=title, description=description, project_id=project_id,
            user_id=user_id)
        task.save_to_db()

    def create_item(self, title, description, task_id, user_id):
        item = Item(title=title, description=description, task_id=task_id,
            user_id=user_id)
        item.save_to_db()

    def create_comment(self, type, comment_text, id, author_id):
        if type=="project":
            comment = ProjectComment(id, author_id, comment_text)
        elif type=="task":
            comment = TaskComment(id, author_id, comment_text)
        elif type=="item":
            comment = ItemComment(id, author_id, comment_text)

        comment.save_to_db()

    def register_user(self, user_name, email, password):
        return self.app.post("/register", data=dict(user_name=user_name,
            email=email, password=password, pass_confirm=password),
            follow_redirects=True)

    def login_user(self, email, password):
        return self.app.post("/login", data=dict(email=email,
            password=password), follow_redirects=True)

    def logout_user(self):
        return self.app.get("/logout", follow_redirects=True)
