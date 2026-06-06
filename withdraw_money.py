# Import SQLite library
import sqlite3

from datetime import datetime

# Ask user for username
username = input("Enter Username: ").strip()

# Ask amount to withdraw
amount = float(input("Enter Amount To Withdraw: "))

# Connect to database
conn = sqlite3.connect("wallet.db")

# Create cursor
cursor = conn.cursor()

# Get current balance of the user
cursor.execute(
    "SELECT balance FROM users WHERE username=?",
    (username,)
)

# Fetch balance from database
current_balance = cursor.fetchone()[0]

# Check if user has enough money
if amount <= current_balance:

    # Calculate new balance
    new_balance = current_balance - amount

    # Get current date and time
    now = datetime.now()

# Store date
    date = now.strftime("%d-%m-%Y")

# Store time
    time = now.strftime("%H:%M:%S")

    # Update balance in database
    cursor.execute(
        "UPDATE users SET balance=? WHERE username=?",
        (new_balance, username)
    )

    # Save transaction record
    cursor.execute(
    """
    INSERT INTO transactions
    (username, amount, type, date, time)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        username,
        amount,
        "Debit",
        date,
        time
    )
)
    # Save changes
    conn.commit()

    print("Money Withdrawn Successfully!")
    print("New Balance =", new_balance)

else:

    print("Insufficient Balance!")

# Close database connection
conn.close()