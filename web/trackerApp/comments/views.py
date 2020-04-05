from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required, current_user

from trackerApp.models import Project, ProjectComment, Task, TaskComment, Item, ItemComment
from trackerApp.comments.forms import AddCommentForm

comments = Blueprint("comments", __name__)

@comments.route("/add_project_note/<project_title>", methods=["GET", "POST"])
@login_required
def add_project_comment(project_title):
    form = AddCommentForm()

    if form.validate_on_submit():
        project = Project.find_by_title(project_title, current_user.user_id)
        comment = ProjectComment(project.project_id, current_user.user_id,
            form.comment.data)
        comment.save_to_db()
        return redirect(url_for("projects.overview", title=project_title))

    return render_template("comments/add.html", form=form, title=project_title,
        action="create")

@comments.route("/project_note/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_project_comment(id):
    form = AddCommentForm()
    form.submit.label.text = "Update"
    comment = ProjectComment.find_by_id(id, current_user.user_id)

    if form.validate_on_submit():
        comment.comment_text = form.comment.data
        comment.save_to_db()
        return redirect(url_for("projects.overview", title=comment.project.title))
    elif request.method == "GET":
        form.comment.data = comment.comment_text

    return render_template("comments/add.html", form=form, title=comment.project.title,
        action="update")


@comments.route("/add_task_note/<task_title>", methods=["GET", "POST"])
@login_required
def add_task_comment(task_title):
    form = AddCommentForm()

    if form.validate_on_submit():
        task = Task.find_by_title(task_title, current_user.user_id)
        comment = TaskComment(task.task_id, current_user.user_id,
            form.comment.data)
        comment.save_to_db()
        return redirect(url_for("tasks.overview", title=task_title))

    return render_template("comments/add.html", form=form, title=task_title,
        action="create")

@comments.route("/task_note/<int:id>", methods=["GET", "POST"])
@login_required
def update_task_comment(id):
    form = AddCommentForm()
    form.submit.label.text = "Update"
    comment = TaskComment.find_by_id(id, current_user.user_id)

    if form.validate_on_submit():
        comment.comment_text = form.comment.data
        comment.save_to_db()
        return redirect(url_for("tasks.overview", title=comment.task.title))
    elif request.method == "GET":
        form.comment.data = comment.comment_text

    return render_template("comments/add.html", form=form, title=comment.task.title,
        action="update")

@comments.route("/add_item_note/<item_title>/update", methods=["GET", "POST"])
@login_required
def add_item_comment(item_title):
    form = AddCommentForm()

    if form.validate_on_submit():
        item = Item.find_by_title(item_title, current_user.user_id)
        comment = ItemComment(item.item_id, current_user.user_id,
            form.comment.data)
        comment.save_to_db()
        return redirect(url_for("items.overview", title=item_title))

    return render_template("comments/add.html", form=form, title=item_title,
        action="create")

@comments.route("/item_note/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_item_comment(id):
    form = AddCommentForm()
    form.submit.label.text = "Update"
    comment = ItemComment.find_by_id(id, current_user.user_id)

    if form.validate_on_submit():
        comment.comment_text = form.comment.data
        comment.save_to_db()
        return redirect(url_for("items.overview", title=comment.item.title))
    elif request.method == "GET":
        form.comment.data = comment.comment_text

    return render_template("comments/add.html", form=form, title=comment.item.title,
        action="update")
