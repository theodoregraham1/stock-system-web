"""shop management application"""

import sqlite3

from flask import Flask, request, render_template, session, redirect, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
con = sqlite3.connect("tutorial.db")
cur = con.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    """Homepage for application"""

    # User reached route via GET
    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    """Login page for application"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
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
        res = cur.execute("SELECT password, id FROM users WHERE username = ?", request.form.get("username"))
        rows = res.fetchall()

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

    # User reached route via GET
    else:
        return render_template("login.html")
    

@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register page for application"""

     # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        # Register a new user

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/register")

        # Ensure username is not taken
        usernames = []

        res = cur.execute("SELECT username FROM users")
        rows = res.fetchall()

        for row in rows:
            usernames.append(row["username"])

        if request.form.get("username") in usernames:
            flash("Username taken")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/register")

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            flash("Must confirm password")
            return redirect("/register")

        # Ensure passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords must match")
            return redirect("/register")

        # Generate password hash
        password_hash = generate_password_hash(request.form.get("password"))

        cur.execute("INSERT INTO users(username, hash) VALUES (?, ?)", request.form.get("username"), password_hash)
        con.commit()

        # Log user in
        res = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = res.fetchall()

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash confirmation
        flash("Registration completed")

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET 
    else:
        return render_template("register.html")