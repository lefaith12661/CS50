import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    # obtain user_id
    user_id = session["user_id"]

    # information we want to display
    items = db.execute(
        "SELECT symbol, name, SUM(shares) as ttl_shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    # what we like to receive
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = cash

    for item in items:
        total += item["price"] * item["ttl_shares"]

    # pass into index.html
    return render_template("index.html", items=items, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        # use lookup function to look up the input symbol
        stock = lookup(symbol)

        # check for valid input
        if not symbol:
            return apology("Provide Symbol")
        elif not stock:
            return apology("Symbol Does Not Exist")

        # share must be int
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Share Must Be Integer")

        # shares have to be greater than 0
        if shares <= 0:
            return apology("Number of Shares Not Allowed")

        # obtain user_id
        user_id = session["user_id"]
        # select the cash amount that a user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # user's total transaction
        stock_name = stock["name"]
        stock_price = stock["price"]
        total_tran = shares * stock_price

        # check if user has enough cash
        if cash < total_tran:
            return apology("Not Enough Cash")
        else:
            # update user cash in users
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_tran, user_id)
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                       user_id, stock_name, shares, stock_price, "buy", symbol)

        # redirect user
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # obtain user_id
    user_id = session["user_id"]

    # select information we want to display
    transactions = db.execute("SELECT type, symbol, price, shares, time FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", transactions=transactions, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # check user input
        if not symbol:
            return apology("Provide Symbol")

        stock = lookup(symbol.upper())

        if not stock:
            return apology("Symbol Does Not Exist")

        return render_template("quoted.html", usd=usd, name=stock["name"], price=stock["price"], symbol=stock["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # access form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # If any field is left blank, return an apology
        if not username:
            return apology("Missing Username")
        elif not password:
            return apology("Missing Password")
        elif not confirmation:
            return apology("Missing Confirmation")

        # If password and confirmation don’t match, return an apology
        if password != confirmation:
            return apology("Passwords Do Not Match")

        hash = generate_password_hash(password)

        try:
            # insert data into database
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            # go back to homepage
            return redirect("/")
        except:
            # If the username is already taken, return an apology
            return apology("Username is already taken")

        # keeps track of which user is logged in
        session["user_id"] = new_user

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # check for only positive int
        if shares <= 0:
            return apology("Shares cannot be less than 1")

        item_price = lookup(symbol)["price"]
        item_name = lookup(symbol)["name"]
        price = shares * item_price

        current_shares = db.execute(
            "SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[0]["shares"]

        if current_shares < shares:
            return apology("Not Enough Shares")

        # update user's cash
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + price, user_id)
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES(?, ?, ?, ?, ?, ?)",
                   user_id, item_name, -shares, item_price, "sell", symbol)

        return redirect("/")
    else:
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)


@app.route("/edit_cash", methods=["GET", "POST"])
@login_required
def edit_cash():
    """Allow users to add/subtract cash to/from their account"""
    if request.method == "POST":
        edit_cash = int(request.form.get("edit_cash"))

        # checking user input
        if not edit_cash:
            return apology("Provide amount")

        # provide user_id
        user_id = session["user_id"]

        # select the cash amount that a user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # total cash
        total_cash = cash + edit_cash

        # update user cash in users
        db.execute("UPDATE users SET cash = ? WHERE id = ?", total_cash, user_id)

        return redirect("/")

    else:
        return render_template("edit_cash.html")