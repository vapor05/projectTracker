from flask import render_template, url_for, Blueprint, redirect
from flask_login import login_required, current_user

from trackerApp.models import Project
from trackerApp.projects.forms import StartProjectForm


projects = Blueprint("projects", __name__)

@projects.route("/create_project", methods=["GET", "POST"])
@login_required
def create_project():
    form = StartProjectForm()

    if form.validate_on_submit():

        if Project.find_by_title(form.title.data, current_user.user_id) == None:
            project = Project(title = form.title.data,
                description = form.description.data, user_id = current_user.user_id)
            project.save_to_db()
            return redirect(url_for("users.home"))
    return render_template("projects/create.html", form=form)

@projects.route("/project_overview/<title>", methods=["GET", "POST"])
@login_required
def overview(title):
    project = Project.find_by_title(title, current_user.user_id)
    return render_template("projects/overview.html", project=project)
