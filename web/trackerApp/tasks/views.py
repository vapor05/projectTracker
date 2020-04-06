from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required, current_user

from trackerApp.models import Task, Project
from trackerApp.tasks.forms import AddTaskForm

tasks = Blueprint("tasks", __name__)

@tasks.route("/add_task/<project_title>", methods=["GET", "POST"])
@login_required
def add_task(project_title):
    form = AddTaskForm()

    if form.validate_on_submit():

        if Task.find_by_title(form.title.data, current_user.user_id) == None:
            project = Project.find_by_title(project_title, current_user.user_id)
            task = Task(title=form.title.data, description=form.description.data,
                project_id=project.project_id, user_id=current_user.user_id)
            task.save_to_db()

        return redirect(url_for("tasks.overview", title=task.title))

    return render_template("tasks/add.html", form=form, project_title=project_title,
        action="create")

@tasks.route("/task_overview/<title>", methods=["GET", "POST"])
@login_required
def overview(title):
    task = Task.find_by_title(title, current_user.user_id)
    return render_template("tasks/overview.html", task=task)

@tasks.route("/task/<title>/update", methods=["GET", "POST"])
@login_required
def update(title):
    form = AddTaskForm()
    form.submit.label.text = "Update"
    task = Task.find_by_title(title, current_user.user_id)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.save_to_db()
        return redirect(url_for("tasks.overview", title=task.title))
    elif request.method == "GET":
        form.title.data = title
        form.description.data = task.description

    return render_template("tasks/add.html", form=form, project_title=task.project.title,
        action="update")

@tasks.route("/task/<title>/delete", methods=["GET", "POST"])
@login_required
def delete(title):
    task = Task.find_by_title(title, current_user.user_id)
    project = task.project
    task.delete()
    return redirect(url_for("projects.overview", title=project.title))
