from flask import render_template, Blueprint

core_views = Blueprint("core", __name__)

@core_views.route("/")
def index():
    return render_template("core/index.html")
