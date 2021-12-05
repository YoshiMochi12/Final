import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///walkmates.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        weekly_miles = request.form.get("weekly_miles")
        full_name = request.form.get("full_name")
        location = request.form.get("location")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password == "" or confirmation == "":
            flash("Please choose a password")
            return redirect("/register")
        if password != confirmation: 
            flash("The passwords do not match")
            return redirect("/register")
        if email == "":
            flash("Please enter an email")
            return redirect("/register")
        if weekly_miles == "":
            flash("Please enter a value")
            return redirect("/register")
        if full_name == "":
            flash("Please enter your full name")
            return redirect("/register")
        if location == "":
            flash("Please enter the area you reside in")
            return redirect("/register")
        if phone_number == "":
            flash("Please enter a valid phone number")
            return redirect("/register")
        if len(db.execute("SELECT * FROM users WHERE email=?", email)) > 0:
            flash("You have already registered with this email")
        return redirect("/login")
    else:
        return render_template("register.html")

# Code modified from finance app.py login 

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
           flash("Email Required")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password Required")

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Redirect user to home page
        return redirect("/register")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/")
def table():
    return render_template("table.html")

@app.route("/dashboard", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        form = request.form
        search_value = form["search_string"]
        search = "%{0}%".format(search_value)
        results = User.query.filter(User.location.like(search)).all()
        return render_template("dashboard.html", locations=results, legend="Search Results")
    else:
        return redirect("/")
