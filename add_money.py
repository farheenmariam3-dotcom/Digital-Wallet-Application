# Import SQLite library
import sqlite3

# Import datetime module
from datetime import datetime

# Get current date and time
now = datetime.now()

# Store date
date = now.strftime("%d-%m-%Y")

# Store time
time = now.strftime("%H:%M:%S")

# Ask which user wants to add money
username = input("Enter Username: ").strip()

# Ask amount to add
amount = float(input("Enter Amount To Add: "))

# Connect to database
conn = sqlite3.connect("wallet.db")

# Create cursor
cursor = conn.cursor()

# Get current balance of user
cursor.execute(
    "SELECT balance FROM users WHERE username=?",
    (username,)
)

# Fetch current balance
current_balance = cursor.fetchone()[0]

# Calculate new balance
new_balance = current_balance + amount

# Update balance in database
cursor.execute(
    "UPDATE users SET balance=? WHERE username=?",
    (new_balance, username)
)

# Save transaction in transactions table
cursor.execute(
    """
    INSERT INTO transactions
    (username, amount, type, date, time)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        username,
        amount,
        "Credit",
        date,
        time
    )
)


# Save changes
conn.commit()

# Close database
conn.close()

# Show new balance
print("Money Added Successfully!")
print("New Balance =", new_balance)