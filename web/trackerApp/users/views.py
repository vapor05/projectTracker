from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from trackerApp import db
from trackerApp.models import User
from trackerApp.users.forms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data,
                    user_name = form.user_name.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("users.login"))
    return render_template("users/register.html", form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("users.home")

            return redirect(next)
    return render_template("users/login.html", form=form)

@users.route("/home", methods=["GET", "POST"])
def home():
    return render_template("users/home.html")
