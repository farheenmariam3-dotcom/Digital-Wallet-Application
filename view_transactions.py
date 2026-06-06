# Import SQLite
import sqlite3

# Connect to database
conn = sqlite3.connect("wallet.db")

# Create cursor
cursor = conn.cursor()

# Get all transactions
cursor.execute("SELECT * FROM transactions")

# Fetch all records
transactions = cursor.fetchall()

# Print transactions
print(transactions)

# Close database
conn.close()