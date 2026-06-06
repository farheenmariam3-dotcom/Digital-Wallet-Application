# This imports SQLite so Python can work with databases
import sqlite3

# Connect to wallet.db
# If wallet.db doesn't exist, SQLite will create it automatically
conn = sqlite3.connect("wallet.db")

# Cursor is used to execute SQL commands
cursor = conn.cursor()

# Create a table called users
# IF NOT EXISTS prevents errors if the table already exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    balance REAL DEFAULT 0
)
""")

# Create transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    type TEXT,
    date TEXT,
    time TEXT
)
""")

# Save changes permanently
conn.commit()

# Close database connection
conn.close()

# Display success message
print("Database Created Successfully!")