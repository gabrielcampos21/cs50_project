import datetime
from helpers import login_required
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = SQL("sqlite:///musics.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
@login_required
def index():
    """Show main page"""
    return render_template("index.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out")
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password were submitted
        if not username or not password:
            return "Please provide both username and password."

        # Check if the user exists in the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1:
            return "Invalid username or password."

        user = rows[0]

        # Check if the provided password is correct
        if not check_password_hash(user["hash"], password):
            return "Invalid username or password."

        # Authentication successful, store the user ID in the session
        session["user_id"] = user["id"]

        flash("Logged!")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if (request.method == "GET"):
        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    email_confirmation = request.form.get("email_confirmation")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # Ensure username was submitted
    if not username:
        return "must provide username"

    # Ensure password was submitted
    if not password:
        return "must provide password"

    if password != confirmation:
        return "passwords do not match"

    # Ensure email was submitted
    if not email:
        return "must provide email"

    if email != email_confirmation:
        return "emails do not match"

    if len(request.form.get("password")) < 8:
        return "passwords need to have at least 8 of length"

    # Ensure username is unique
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    if (len(rows) != 0):
        return "this username is already taken"

    # Ensure email is unique
    rows = db.execute("SELECT * FROM users WHERE email = ?", email)
    if (len(rows) != 0):
        return "this email is already taken"

    # get hashed password to be stored
    hashed_pass = generate_password_hash(request.form.get("password"))

    # add new user to the db
    db.execute("INSERT INTO users(username, hash, email, creation_date) VALUES(?, ?, ?, ?)",
                username, hashed_pass, email, datetime.datetime.now())

    flash("You are registered!")
    session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]
    return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change account settings"""

    if request.method == "GET":
        return render_template("settings.html")
    else:
        new_password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure new password and confirmation were submitted
        if not new_password:
            return "Please provide a new password."

        if new_password != confirmation:
            return "Passwords do not match."

        if len(request.form.get("password")) < 8:
                return "passwords need to have at least 8 of length"

        # Generate the hashed password
        hashed_pass = generate_password_hash(new_password)

        # Update the user's password in the database
        db.execute("UPDATE users SET hash=? WHERE id=?", hashed_pass, session['user_id'])

        flash("Password changed successfully.")
        return redirect("/settings")


@app.route("/recommendations", methods=["GET", "POST"])
@login_required
def recommendations():
    return render_template("layout.html")


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    return render_template("layout.html")


@app.route("/playlists", methods=["GET", "POST"])
@login_required
def playlists():
    return render_template("layout.html")