from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3

# Create Flask application
app = Flask(__name__)

app.secret_key = "digital_wallet_secret"

# Login Page
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Connect database
        conn = sqlite3.connect("wallet.db")

        # Create cursor
        cursor = conn.cursor()

        # Check username and password
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        # If user exists
        if user:

            session["username"] = username

            return redirect(url_for("dashboard"))

        else:

            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("wallet.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (username, password, balance)
            VALUES (?, ?, ?)
            """,
            (
                username,
                password,
                0
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("register.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )

@app.route("/balance")
def balance():

    if "username" not in session:
        return redirect(url_for("home"))

    conn = sqlite3.connect("wallet.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE username=?",
        (session["username"],)
    )

    result = cursor.fetchone()

    conn.close()

    return render_template(
        "balance.html",
        balance=result[0]
    )

@app.route("/add_money", methods=["GET", "POST"])
def add_money():

    if "username" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        amount = float(request.form["amount"])

        conn = sqlite3.connect("wallet.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT balance FROM users WHERE username=?",
            (session["username"],)
        )

        current_balance = cursor.fetchone()[0]

        new_balance = current_balance + amount

        cursor.execute(
            "UPDATE users SET balance=? WHERE username=?",
            (new_balance, session["username"])
        )

        now = datetime.now()

        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        cursor.execute(
                """
                INSERT INTO transactions
                (username, amount, type, date, time)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session["username"],
                    amount,
                    "Credit",
                    date,
                    time
                )
            )
        conn.commit()
        conn.close()

        return redirect(url_for("balance"))

    return render_template("add_money.html")

@app.route("/withdraw_money", methods=["GET", "POST"])
def withdraw_money():

    if "username" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        amount = float(request.form["amount"])

        conn = sqlite3.connect("wallet.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT balance FROM users WHERE username=?",
            (session["username"],)
        )

        current_balance = cursor.fetchone()[0]

        if amount <= current_balance:

            new_balance = current_balance - amount

            cursor.execute(
                "UPDATE users SET balance=? WHERE username=?",
                (new_balance, session["username"])
            )

            now = datetime.now()

            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%H:%M:%S")

            cursor.execute(
                """
                INSERT INTO transactions
                (username, amount, type, date, time)
                VALUES (?, ?, ?, ?, ?)
                """,
            (
                session["username"],
                amount,
                "Debit",
                date,
                time
            )
            )   
            


            conn.commit()

            conn.close()

            return redirect(url_for("balance"))

        else:

            conn.close()

            return "Insufficient Balance"

    return render_template("withdraw_money.html")

@app.route("/transactions")
def transactions():

    if "username" not in session:
        return redirect(url_for("home"))

    conn = sqlite3.connect("wallet.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM transactions WHERE username=?",
        (session["username"],)
    )

    transactions = cursor.fetchall()

    conn.close()

    return render_template(
        "transactions.html",
        transactions=transactions
    )

@app.route("/analytics")
def analytics():

    conn = sqlite3.connect("wallet.db")
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT SUM(amount)
    FROM transactions
    WHERE username=? AND type='Credit'
    """,
    (session["username"],)
)
    
    cursor.execute(
    """
    SELECT SUM(amount)
    FROM transactions
    WHERE username=? AND type='Debit'
    """,
    (session["username"],)
)
    
    total_credit = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type='Debit'"
    )
    total_debit = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT balance FROM users WHERE username=?",
        (session["username"],)
    )
    balance = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "analytics.html",
        total_credit=total_credit,
        total_debit=total_debit,
        balance=balance
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))

# Run Application
if __name__ == "__main__":
    app.run(debug=True)