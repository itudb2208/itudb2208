from flask import (
   Blueprint, flash, redirect, render_template, request,url_for, session
)
from flask_login import login_required,login_user, logout_user
from project.db import get_db
from project import login_manager,User

bp = Blueprint('login', __name__, url_prefix='/')

USERS = {} # users will be loaded from database via login() method

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

@bp.route("/login", methods=["GET", "POST"])
def login():

    database = get_db()
    cursor = database.cursor()
    res = cursor.execute("SELECT * FROM Users") # all rows from Users table

    for user in res.fetchall():
        USERS[int(user["userID"])] = User(user["username"],user["password"],user["userID"]) 

    if request.method == "POST":
        username = request.form["username"] # username and password field from the form in HTML
        password = request.form["password"]

        for user in USERS.values():
            if username == user.name and password == user.password:
                login_user(user)
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("teams.index"))
        flash("Could not log in.")

    else:
        session.pop('_flashes', None) # clear flash messages

    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))
