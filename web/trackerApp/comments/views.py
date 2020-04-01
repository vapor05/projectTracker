from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user

from trackerApp.models import Project, ProjectComment
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

    return render_template("comments/add.html", form=form, project_title=project_title)
