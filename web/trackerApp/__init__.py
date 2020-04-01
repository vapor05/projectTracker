import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "mySecertKey"

# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://%s:%s@%s/%s" \
    % (os.environ.get("DB_USER", ""), os.environ.get("DB_PASSWORD", ""),
     os.environ.get("DB_HOST", ""), os.environ.get("DB_NAME"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from trackerApp.core.views import core
from trackerApp.users.views import users
from trackerApp.projects.views import projects
from trackerApp.tasks.views import tasks
from trackerApp.items.views import items
from trackerApp.comments.views import comments

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(projects)
app.register_blueprint(tasks)
app.register_blueprint(items)
app.register_blueprint(comments)
