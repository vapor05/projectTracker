from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user

from trackerApp.models import Task, Project
from trackerApp.tasks.forms import AddTaskForm

tasks = Blueprint("tasks", __name__)

@tasks.route("/add_task/<project_title>", methods=["GET", "POST"])
@login_required
def add_task(project_title):
    form = AddTaskForm()

    if form.validate_on_submit():

        if Task.find_by_title(form.title.data) == None:
            project = Project.find_by_title(project_title)
            task = Task(title=form.title.data, description=form.description.data,
                project_id=project.project_id, user_id=current_user.user_id)
            task.save_to_db()

        return redirect(url_for("projects.overview", title=project_title))

    return render_template("tasks/add.html", form=form, project_title=project_title)

@tasks.route("/task_overview/<title>", methods=["GET", "POST"])
def overview(title):
    task = Task.find_by_title(title)
    return render_template("tasks/overview.html", task=task)
