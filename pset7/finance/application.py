from cs50 import SQL
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = ("no-cache, "
                                             "no-store, "
                                             "must-revalidate")
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    # load user porfolio
    portfolios = db.execute(
            "SELECT symbol, shares, "
            "price, total from portfolios WHERE id=:id",
            id=session["user_id"])

    # gross = cash + shares value
    gross = 0

    # update price of each stock + the total shares value
    for portfolio in portfolios:
        symbol = portfolio["symbol"]
        shares = portfolio["shares"]
        update = lookup(symbol)
        price = update["price"]
        total = float(price) * float(shares)
        gross += total
        db.execute(
                "UPDATE portfolios SET price=:price, total=:total "
                "WHERE id=:id AND symbol=:symbol",
                price=usd(price),
                total=usd(total),
                id=session["user_id"],
                symbol=symbol)

    # load user profile after update of price and total shares value
    stocks = db.execute(
            "SELECT * from portfolios WHERE id=:id",
            id=session["user_id"])

    # load user balance
    cash = db.execute(
            "SELECT cash from users WHERE id=:id",
            id=session["user_id"])

    # get format from dict
    cash = cash[0]["cash"]

    # calculating gross
    gross += cash

    return render_template(
            "index.html",
            stocks=stocks,
            cash=usd(cash),
            gross=usd(gross))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # if user reached route via POST
    # (as by submitting a form via POST)
    if request.method == "POST":

        # look fer a given symbol
        quote = lookup(request.form.get("symbol"))

        # if given symbol is invalid
        if not quote:
            return apology("invalid symbol")

        # if the input is not a positive integer
        order_t = request.form.get("shares")
        if order_t.isdigit():
            order = int(request.form.get("shares"))
        else:
            return apology("only digits allowed")

        if order <= 0:
            return apology("you can only buy shares greater than 1")

        # get user balance
        balance = db.execute(
                "SELECT cash FROM users WHERE id=:id",
                id=session["user_id"])

        # if no balance
        if not balance:
            return apology("no balance")

        # if low balance
        if quote["price"] * order > float(balance[0]["cash"]):
            return apology("no sufficient funds")

        # subtract from current balance
        # due to successful order fulfillment
        db.execute(
                "UPDATE users SET cash=cash - :cash WHERE id=:id",
                id=session["user_id"],
                cash=quote["price"] * float(order))

        # check if share available in portfolio
        buy_order = db.execute(
                "SELECT shares FROM portfolios "
                "WHERE id=:id AND symbol=:symbol",
                id=session["user_id"],
                symbol=quote["symbol"])

        # if share available update shares count
        if buy_order:
            increment = buy_order[0]["shares"] + order
            db.execute(
                    "UPDATE portfolios SET shares=:shares "
                    "WHERE id=:id AND symbol=:symbol",
                    shares=increment, id=session["user_id"],
                    symbol=quote["symbol"])

        # if new share create a new entry
        else:
            db.execute(
                    "INSERT INTO portfolios (id, symbol, name, "
                    "shares, price) VALUES (:id, :symbol, :name, "
                    ":shares, :price)",
                    id=session["user_id"],
                    symbol=quote["symbol"],
                    name=quote["name"],
                    shares=order,
                    price=usd(quote["price"]))

        # update user order histroy
        db.execute(
                "INSERT INTO histories (id, symbol, shares, "
                "price) VALUES (:id, :symbol, :shares, :price)",
                id=session["user_id"],
                symbol=quote["symbol"],
                shares=order,
                price=usd(quote["price"]))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET
    # (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # pull history records of buy/sell order of a user
    histories = db.execute(
            "SELECT * FROM histories WHERE id=:id",
            id=session["user_id"])

    # push history records  of buy/sell order of a user
    # to history page
    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST
    # (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute(
                "SELECT * FROM users "
                "WHERE username = :username",
                username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid username and/or password")

        # ensure username exists and password is correct
        if not pwd_context.verify(
                request.form.get("password"),
                rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET
    # (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if user reached route via POST
    # (as by submitting a form via POST)
    if request.method == "POST":

        # look for a given symbol
        quote = lookup(request.form.get("symbol"))

        # if given symbol is invalid
        if not quote:
            return apology("invalid symbol")

        # return given symbol information
        return render_template("quoted.html", symbol=quote)

    # if user reached route via POST
    # (as by submitting a form via POST)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST
    # (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username!")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password!")

        # Require that a user input a password
        # and then that same password again
        elif request.form.get("password") != request.form.get("password2"):
            return apology("passwords do not match")

        # query database for username
        result = db.execute(
                "INSERT INTO users (username, hash) "
                "VALUES(:username, :hash)",
                username=request.form.get("username"),
                hash=pwd_context.hash(request.form.get("password")))

        # ensure username exists and password is correct
        if not result:
            return apology("username is taken")

        # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET
    # (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    # if user reached route via POST
    # (as by submitting a form via POST)
    if request.method == "POST":

        # look for a given symbol
        quote = lookup(request.form.get("symbol"))

        # if given symbol is invalid
        if not quote:
            return apology("invalid symbol")

        # if the input is not a positive integer
        order_t = request.form.get("shares")
        if order_t.isdigit():
            order = int(request.form.get("shares"))
        else:
            return apology("only digits allowed")

        if order <= 0:
            return apology("you can only buy shares greater than 1")

        # check if share available in portfolio
        sell_order = db.execute(
                "SELECT shares FROM portfolios "
                "WHERE id=:id AND symbol=:symbol",
                id=session["user_id"], symbol=quote["symbol"])

        # if share is not in portfolio
        if not sell_order:
            return apology("no shares found")

        # if user tries to sell more than what they own
        if order > int(sell_order[0]["shares"]):
            return apology("you cannot sell more than you own")

        # add to current balance
        # due to successful order fulfillment
        db.execute(
                "UPDATE users SET cash=cash + :cash WHERE id=:id",
                id=session["user_id"],
                cash=quote["price"] * float(order))

        # update share count
        shares_left = sell_order[0]["shares"] - order

        # if share count is positive
        if shares_left:
            db.execute(
                    "UPDATE portfolios SET shares=:shares "
                    "WHERE id=:id AND symbol=:symbol",
                    shares=shares_left, id=session["user_id"],
                    symbol=quote["symbol"])

        else:
            # if share count is nil
            db.execute(
                    "DELETE FROM portfolios WHERE id=:id "
                    "AND symbol=:symbol",
                    id=session["user_id"],
                    symbol=quote["symbol"])

        # update user order histroy
        db.execute(
                "INSERT INTO histories (id, symbol, shares, "
                "price) VALUES (:id, :symbol, :shares, :price)",
                id=session["user_id"],
                symbol=quote["symbol"],
                shares=-order,
                price=usd(quote["price"]))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET
    # (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change Password"""

    # if user reached route via POST
    # (as by submitting a form via POST)
    if request.method == "POST":

        # ensure passwords were submitted
        if not request.form.get("password0"):
            return apology("Missing password!")

        if not request.form.get("password1"):
            return apology("Missing password!")

        if not request.form.get("password2"):
            return apology("Missing password!")

        # query database for username
        rows = db.execute(
                "SELECT * FROM users WHERE id=:id",
                id=session["user_id"])

        # ensure username exists and password is correct
        if not pwd_context.verify(
                request.form.get("password0"),
                rows[0]["hash"]):
            return apology("invalid password")

        # Require that a user input a password
        # and then that same password again
        elif request.form.get("password1") != request.form.get("password2"):
            return apology("new passwords do not match")

        # change the password
        db.execute(
                "UPDATE users SET hash=:hash WHERE id=:id",
                id=session["user_id"],
                hash=pwd_context.hash(request.form.get("password1")))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via get
    # (as by clicking a link or via redirect)
    else:
        return render_template("password.html")