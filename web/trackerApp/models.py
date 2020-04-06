from datetime import datetime
from trackerApp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class BaseModel():

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin, BaseModel):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    create_user = db.Column(db.String(80))

    projects = db.relationship("Project", backref="author", lazy=True)

    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id


class Status(db.Model):
    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.String(30))
    description = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)
    create_user = db.Column(db.String(80))

    projects = db.relationship("Project", backref="status_group", lazy=True)


class WorkLevel(BaseModel):

    @classmethod
    def find_by_title(cls, title, user_id):
        return cls.query.filter(cls.title==title, cls.author_id==user_id).first()

    def delete_comments(self, comments):
        for comment in comments:
            comment.delete_from_db()


class Project(db.Model, WorkLevel):
    __tablename__ = "projects"

    user = db.relationship(User)
    status = db.relationship(Status)

    project_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False )
    assigned_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey("status.status_id"), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="tasks", lazy=True)
    comments = db.relationship("ProjectComment", backref="comments", lazy=True)

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.author_id = user_id
        # new projects always start as 'Proposed'
        self.status_id = 1

    def delete(self):
        self.delete_comments(self.comments)
        tasks = self.tasks

        for task in tasks:
            task.delete()

        self.delete_from_db()


class Task(db.Model, WorkLevel):
    __tablename__ = "tasks"

    project = db.relationship(Project)
    user = db.relationship(User)
    status = db.relationship(Status)

    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    assigned_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey("status.status_id"), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("Item", backref="items", lazy=True)
    comments = db.relationship("TaskComment", backref="comments", lazy=True)

    def __init__(self, title, description, project_id, user_id):
        self.title = title
        self.description = description
        self.project_id = project_id
        self.author_id = user_id
        # new tasks always start as 'Proposed'
        self.status_id = 1

    def delete(self):
        self.delete_comments(self.comments)
        items = self.items

        for item in items:
            item.delete()

        self.delete_from_db()


class Item(db.Model, WorkLevel):
    __tablename__ = "items"

    user = db.relationship(User)
    status = db.relationship(Status)
    task = db.relationship(Task)

    item_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status.status_id"), nullable=False)
    assigned_id = db.Column(db.Integer)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship("ItemComment", backref="comments", lazy=True)

    def __init__(self, title, description, task_id, user_id):
        self.title = title
        self.description = description
        self.task_id = task_id
        self.author_id = user_id
        # new items always start as 'Proposed'
        self.status_id = 1

    def delete(self):
        self.delete_comments(self.comments)
        self.delete_from_db()

class ProjectComment(db.Model, BaseModel):
    __tablename__ = "project_comments"

    project = db.relationship(Project)
    user = db.relationship(User)

    project_comment_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    comment_text = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, project_id, user_id, comment_text):
        self.project_id = project_id
        self.author_id = user_id
        self.comment_text = comment_text

    @classmethod
    def find_by_id(cls, project_comment_id, user_id):
        return cls.query.filter(cls.project_comment_id==project_comment_id,
            cls.author_id==user_id).first()

class TaskComment(db.Model, BaseModel):
    __tablename__ = "task_comments"

    task = db.relationship(Task)
    user = db.relationship(User)

    task_comment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    comment_text = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, task_id, user_id, comment_text):
        self.task_id = task_id
        self.author_id = user_id
        self.comment_text = comment_text

    @classmethod
    def find_by_id(cls, task_comment_id, user_id):
        return cls.query.filter(cls.task_comment_id==task_comment_id,
            cls.author_id==user_id).first()


class ItemComment(db.Model, BaseModel):
    __tablename__ = "item_comments"

    item = db.relationship(Item)
    user = db.relationship(User)

    item_comment_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    comment_text = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, item_id, user_id, comment_text):
        self.item_id = item_id
        self.author_id = user_id
        self.comment_text = comment_text

    @classmethod
    def find_by_id(cls, item_comment_id, user_id):
        return cls.query.filter(cls.item_comment_id==item_comment_id,
            cls.author_id==user_id).first()
