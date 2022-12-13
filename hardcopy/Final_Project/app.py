import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from functools import wraps


# __name__ just refers to the name of the current file
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///money_review.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Decorate routes to require login.
# https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# log user in
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# log user out
@app.route("/logout")
def logout():
    # Forget any id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

# register user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # access form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # If any field is left blank, return an apology
        if not username:
            return render_template("error.html", message="Missing Username")
        elif not password:
            return render_template("error.html", message="Missing Password")
        elif not confirmation:
            return render_template("error.html", message="Missing Confirmation")

        # If password and confirmation don’t match, return an apology
        if password != confirmation:
            return render_template("error.html", message="Passwords Do Not Match")

        # Password hashing adds a layer of security
        hash = generate_password_hash(password)

        try:
            # insert data into database
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

            # go back to homepage
            return redirect("/")
        except:
            # If the username is already taken, return an apology
            return render_template("error.html", message="Username is already taken")

        # keeps track of which user is logged in
            session["user_id"] = new_user

    else:
        return render_template("register.html")


# when clicked on home icon, it will navigate to home page
@app.route("/home")
@login_required
def home():
    return render_template("home.html")

# default page after logged in
@app.route("/")
@login_required
def index():
    return render_template("home.html")

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # obtain id
        id = session["user_id"]

        # access form data
        wkly_ttl = request.form.get("total_amount")

        # remember item
        db.execute("UPDATE users SET wkly_ttl = ? WHERE id = ?", wkly_ttl, id)

        # confirmation
        return redirect("/budget")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("budget.html")


@app.route("/calculate", methods=["GET", "POST"])
@login_required
def calculate():
    # obtain id
    id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # access form data
        date = request.form.get("date")
        category = request.form.get("category")
        description = request.form.get("description")
        amount = request.form.get("amount")

        # remember item
        db.execute("INSERT INTO spendings (user_id, date, category, description, amount) VALUES(?, ?, ?, ?, ?)",
                   id, date, category, description, amount)

        # redirect user to summary
        return redirect("/calculate")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # total spending of each item
        grocery_ttl = db.execute("SELECT ROUND(SUM(amount),2) AS sum_gro FROM spendings WHERE category = 'Grocery' AND user_id = ?", id)
        eating_out_ttl = db.execute("SELECT ROUND(SUM(amount),2) AS sum_eat FROM spendings WHERE category = 'Eating Out' AND user_id = ?", id)
        entertainment_ttl = db.execute("SELECT ROUND(SUM(amount),2) AS sum_ent FROM spendings WHERE category = 'Entertainment' AND user_id = ?", id)
        pet_supply_ttl = db.execute("SELECT ROUND(SUM(amount),2) AS sum_pet FROM spendings WHERE category = 'Pet Supply' AND user_id = ?", id)
        other_ttl = db.execute("SELECT ROUND(SUM(amount),2) AS sum_oth FROM spendings WHERE category = 'Other' AND user_id = ?", id)

        return render_template("calculate.html", grocery_ttl=grocery_ttl, eating_out_ttl=eating_out_ttl, entertainment_ttl=entertainment_ttl,
                               pet_supply_ttl=pet_supply_ttl, other_ttl=other_ttl)

# show a summary of the spendings
@app.route("/summary")
@login_required
def summary():
    # obtain id
    id = session["user_id"]

    # select information we want to display
    spendings = db.execute("SELECT id, date, category, description, amount FROM spendings WHERE user_id = ? ORDER BY category", id)
    users = db.execute("SELECT wkly_ttl FROM users WHERE id = ?", id)

    # sum of all items
    sum_all = db.execute("SELECT ROUND(SUM(amount),2) as sum_amount FROM spendings WHERE user_id = ?", id)

    return render_template("summary.html", spendings=spendings, users=users, sum_all=sum_all)

# remove item from summary list
@app.route("/remove", methods=["POST"])
@login_required
def remove():
    # remove spending
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM spendings WHERE id = ?", id)
    return redirect("/summary")




