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
    create_date = db.Column(db.DateTime)
    create_user = db.Column(db.String(80))

    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id
