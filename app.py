

from flask import Flask, request, render_template, session, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Homepage for application"""
    # User reached by GET

    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    """Login page for application"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username not provided")
            return redirect("/login/")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password not provided")
            return redirect("/login/")

        # Query database for username
        rows = db.execute("SELECT password, id FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
            return redirect("/login/")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash confirmation
        flash("Login completed")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/register/", methods=["GET", "POST"])