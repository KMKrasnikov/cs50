import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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
    if request.method == "GET":
        stocks = db.execute("SELECT share, price, number_shares FROM shares WHERE username = (SELECT username FROM users WHERE id = ?)", session["user_id"])
        i = 0
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        total = cash[0]["cash"]
        for stock in stocks:
            price = lookup(stock['share'])
            stock['price'] = price['price']
            stock['total'] = stock['price'] * stock['number_shares']
            stocks[i] = stock
            i += 1
            total += stock['total']
        return render_template("index.html", stocks=stocks, total=total, cash=cash[0]['cash'])
    else:
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quoted = lookup(symbol)
        if quoted is None:
            return apology("You did not enter a stock's symbol or the stock's symbol is not exist", 400)

        price = float(quoted['price'])
        number = request.form.get("shares")
        if len(number) == 0 :
            return apology("Shares can't be a null or a negative number", 400)
        number = int(number)
        total = price * number
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if total > balance[0]['cash']:
            return apology("You don't have enough cash", 400)
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username[0]['username']
        cash = balance[0]['cash'] - total
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        type = "Buy"
        # Input inforfmation of buy into history
        db.execute("INSERT INTO history (username, share, price, number_shares, type_of_transaction, date) VALUES (?, ?, ?, ?, ?, datetime())", username, symbol, price, number, type)
        share = db.execute("SELECT share FROM shares WHERE share LIKE ? AND username = (SELECT username FROM users WHERE id = ?)", symbol, session["user_id"])
        if len(share) == 0:
            db.execute("INSERT INTO shares (username, share, price, number_shares) VALUES (?, ?, ?, ?)", username, symbol, price, number)
        else:
            numb_shares = db.execute("SELECT number_shares FROM shares WHERE share LIKE ? AND username = (SELECT username FROM users WHERE id = ?)", symbol, session["user_id"])
            number_shares = numb_shares[0]['number_shares'] + number
            db.execute("UPDATE shares SET number_shares = ? WHERE share LIKE ? AND username = (SELECT username FROM users WHERE id = ?)", number_shares, symbol, session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        stocks = db.execute("SELECT share, price, number_shares, date, type_of_transaction FROM history WHERE username = (SELECT username FROM users WHERE id = ?)", session["user_id"])
        return render_template("history.html", stocks=stocks)
    else:
        return redirect("/")


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
        quoted = lookup(symbol)
        if quoted is None:
            return apology("You did not enter a stock's symbol or the stock's symbol is not exist", 400)
        return render_template("quoted.html", quoted=quoted['price'])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Check username
        username = request.form.get("username")
        db_username = db.execute("SELECT username FROM users")
        if len(username) == 0 or username in db_username:
            return apology("You did not enter a username or the given username is taken", 400)
        # Check password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if len(password) == 0 or password != confirmation:
            return apology("The password is blank or the entered passwords do not match", 400)

        # Password to hash
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Import username and password hash into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""
    if request.method == "POST":
        old_password = request.form.get("oldpassword")
        # Ensure password was submitted
        if not old_password:
            return apology("must provide password", 400)

        new_password = request.form.get("newpassword")
        if not new_password:
            return apology("must provide password", 400)

        confirm_password = request.form.get("confirmpassword")
        if not confirm_password:
            return apology("must provide password", 400)

        if new_password != confirm_password:
            return apology("new password and confirm passworf must be same", 400)

        # Query database for username
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("invalid old password", 400)

        # Password to hash
        hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)

        # Change password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])
        return redirect("/")
    else:
        return render_template("changepassword.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if symbol is None:
            return apology("You did not have any stocks", 400)
        quoted = lookup(symbol)
        shares = db.execute("SELECT * FROM shares WHERE share LIKE ? AND username = (SELECT username FROM users WHERE id = ?)", symbol, session["user_id"])
        if quoted is None:
            return apology("You did not enter a stock's symbol or the stock's symbol is not exist", 400)
        price = float(quoted['price'])
        number = request.form.get("shares")
        if len(number) == 0:
            return apology("You don't enter number of stocks", 400)
        number = int(number)
        if number > shares[0]['number_shares']:
            return apology("You don't have enough stocks", 400)
        total = price * number
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username[0]['username']
        type = "Sell"
        # Input inforfmation of buy into history
        db.execute("INSERT INTO history (username, share, price, number_shares, type_of_transaction, date) VALUES (?, ?, ?, ?, ?, datetime())", username, symbol, price, number, type)
        cash = balance[0]['cash'] + total
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        number_shares = int(shares[0]['number_shares']) - number
        # Check for zero stocks
        if number_shares == 0:
            db.execute("DELETE FROM shares WHERE share LIKE ? AND username = (SELECT username FROM users WHERE id = ?)", symbol, session["user_id"])
        else:
            db.execute("UPDATE shares SET number_shares = ? WHERE share LIKE ? AND username = (SELECT username FROM users WHERE id = ?)", number_shares, symbol, session["user_id"])
        return redirect("/")
    else:
        shares = db.execute("SELECT share FROM shares WHERE username = (SELECT username FROM users WHERE id = ?) ", session["user_id"])
        return render_template("sell.html", shares=shares)
