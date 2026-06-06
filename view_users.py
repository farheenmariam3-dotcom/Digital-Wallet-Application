# Import SQLite library
import sqlite3

# Connect to database
conn = sqlite3.connect("wallet.db")

# Create cursor
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")

# Fetch all rows
users = cursor.fetchall()

# Print users
print(users)

# Close database
conn.close()