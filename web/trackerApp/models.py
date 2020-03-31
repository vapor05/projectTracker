from datetime import datetime
from trackerApp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Status(db.Model):
    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.String(30))
    description = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)
    create_user = db.Column(db.String(80))

    projects = db.relationship("Project", backref="status_group", lazy=True)


class Project(db.Model):
    __tablename__ = "projects"

    user = db.relationship(User)
    status = db.relationship(Status)

    project_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    assigned_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey("status.status_id"), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    create_date  = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="tasks", lazy=True)

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.author_id = user_id
        # new projects always start as 'Proposed'
        self.status_id = 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()


class Task(db.Model):
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

    def __init__(self, title, description, project_id, user_id):
        self.title = title
        self.description = description
        self.project_id = project_id
        self.author_id = user_id
        # new tasks always start as 'Proposed'
        self.status_id = 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
