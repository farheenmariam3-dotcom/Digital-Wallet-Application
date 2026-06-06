# Import SQLite library
import sqlite3

# Ask for username
username = input("Enter Username: ").strip()

# Connect to database
conn = sqlite3.connect("wallet.db")

# Create cursor
cursor = conn.cursor()

# Get user's balance
cursor.execute(
    "SELECT balance FROM users WHERE username=?",
    (username,)
)

result = cursor.fetchone()

print("DEBUG:", result)

if result:
    balance = result[0]
    print("Current Balance =", balance)
else:
    print("User Not Found!")

# Close database
conn.close()