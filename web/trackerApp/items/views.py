from flask import render_template, Blueprint, redirect, url_for, request
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

        return redirect(url_for("items.overview", title=item.title))

    return render_template("items/add.html", form=form, task_title=task_title,
        action="create")


@items.route("/item_overview/<title>", methods=["GET", "POST"])
@login_required
def overview(title):
    item = Item.find_by_title(title, current_user.user_id)
    return render_template("items/overview.html", item=item)

@items.route("/item/<title>/update", methods=["GET", "POST"])
@login_required
def update(title):
    form = AddItemForm()
    form.submit.label.text = "Update"
    item = Item.find_by_title(title, current_user.user_id)

    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.save_to_db()
        return redirect(url_for("items.overview", title=item.title))
    elif request.method == "GET":
        form.title.data = title
        form.description.data = item.description

    return render_template("items/add.html", form=form, task_title=item.task.title,
        action="update")
