from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user

from trackerApp.models import Item, Task
from trackerApp.items.forms import AddItemForm

items = Blueprint("items", __name__)

@items.route("/add_item/<task_title>", methods=["GET", "POST"])
@login_required
def add(task_title):
    form = AddItemForm()

    if form.validate_on_submit():

        if not Item.find_by_title(form.title.data, current_user.user_id):
            task = Task.find_by_title(task_title, current_user.user_id)
            item = Item(title=form.title.data, description=form.description.data,
                task_id=task.task_id, user_id=current_user.user_id)
            item.save_to_db()

        return redirect(url_for("tasks.overview", title=task_title))

    return render_template("items/add.html", form=form, task_title=task_title)
