import os

from datetime import date
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    userID = session['user_id']

    userPurchases =  db.execute("SELECT symbol, amount FROM purchaces WHERE user_id = ?", userID)

    valueSum = 0

    for i in range(len(userPurchases)):
        currentData = lookup(userPurchases[i]["symbol"])
        value = currentData["price"] * userPurchases[i]["amount"]
        userPurchases[i]["currentPrice"] = usd(currentData["price"])
        
        userPurchases[i]["value"] = usd(value)
        
        valueSum += value

    cash = db.execute("SELECT cash FROM users WHERE id = ?", userID)
    cash = cash[0]["cash"]

    total = float(cash) + float(valueSum)
    
    cash = usd(cash)
    
    total = usd(total)

    return render_template("index.html", rows = userPurchases, cash = cash, total = total)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        quote = lookup(symbol)

        if not symbol:
            return apology("Symbol can't be blank.", 400)
        elif quote == None:
            return apology("Please enter a valid symbol.", 400)
        elif not shares:
            return apology("Missing shares.", 400)
        elif not shares.isdigit() or int(shares) < 0:
            return apology("Shares should not be fractional, negative, and non-numeric.", 400)
        else:
            shares = int(shares)
            name = quote["name"]
            price = quote["price"]
            user = session["user_id"]
            money = db.execute("SELECT cash FROM users WHERE id = :id", id=user)
            cash = money[0]["cash"]
            total = shares * price

            if total > cash:
                return apology("Not enough cash. Can't afford!", 400)
            else:
                balance = cash - total
                timestamp = date.today().strftime('%Y-%m-%d %H:%M:%S')

                db.execute("INSERT INTO purchaces (symbol, user_id, amount, price, date_time) VALUES (?, ?, ?, ?, ?)",
                           symbol, user, shares, price, timestamp)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user)
                flash("Successfully bought!")
                return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    purchases = db.execute("SELECT price, symbol, amount FROM purchaces WHERE user_id = ?", session["user_id"])
    sells = db.execute("SELECT price, symbol, amount FROM sells WHERE user_id = ?", session["user_id"])
    
    return render_template("history.html", purchases = purchases, sells = sells)


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

"""
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    
    if request.method == "POST":

        quoteSymbol = request.form.get("symbol")
        
        if not quoteSymbol:
            return apology("must provide stock name", 400)
        
        quotes = lookup(quoteSymbol)

        if quotes is None:
            return apology("No quotes for provided stock")

        return render_template("quoted.html", name = quotes['name'], symbol = quotes['symbol'], price = quotes['price'])
    else:

        return render_template("quote.html")
        
"""

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Please provide a valid symbol", 400)
        else:
            name = quote["name"]
            symbol = quote["symbol"]
            price = quote["price"]
            price = usd(price)

            return render_template("quoted.html", name=name, symbol=symbol, price=price)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("invalid username", 400)

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return apology("passwords don't match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(request.form.get("password")))

        session['user_id'] = db.execute("SELECT id FROM users WHERE username = ?", username)

        return redirect("/login")
    else:
        return render_template("register.html")



    
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    rows = db.execute("SELECT symbol, amount FROM purchaces WHERE user_id = ?", session["user_id"])

    symbols = []
    for row in rows:
        symbols.append(row["symbol"])


    if request.method == "POST":
        inputSymbol = request.form.get("symbol")

        if inputSymbol not in symbols:
            apology("you don't own that share", 400)

        inputNumber = request.form.get("shares")
        inputNumber = int(inputNumber)

        for row in rows:
            if row["symbol"] == inputSymbol:
                owned = row["amount"]
        
        
        condition = inputNumber > owned
        print(condition)

        if inputNumber < 0:
            apology("you can't sell less than 1 share", 400)
        elif inputNumber > owned:
            apology("you don't own that much of that share", 400)
        elif condition:
            apology("you don't own that much of that share", 400)

        currentPrice = lookup(inputSymbol)["price"]

        earned = inputNumber * currentPrice

        cash = (db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"]))[0]['cash']
        
        total = cash + earned

        db.execute("UPDATE users SET cash = ? WHERE id = ?", total, session["user_id"])

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        db.execute("INSERT INTO sells (user_id, price, symbol, amount, date_time) VALUES (?, ?, ?, ?, ?)", session["user_id"], currentPrice, inputSymbol, inputNumber, d1)

        return redirect("/")
    else:
        return render_template("sell.html", symbols = symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
