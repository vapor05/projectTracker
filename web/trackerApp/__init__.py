from flask import Flask

from trackerApp.core.views import core_views

app = Flask(__name__)
app.config["SECRET_KEY"] = "mySecertKey"

app.register_blueprint(core_views)
