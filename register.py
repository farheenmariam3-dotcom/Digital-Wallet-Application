# Import SQLite library
import sqlite3

# Function to register a new user
def register_user():

    # Ask user to enter username
    username = input("Enter Username: ").strip()

    # Ask user to enter password
    password = input("Enter Password: ")

    # Connect to wallet database
    conn = sqlite3.connect("wallet.db")

    # Create cursor to run SQL commands
    cursor = conn.cursor()

    # Insert username and password into users table
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    # Save changes
    conn.commit()

    # Close database connection
    conn.close()

    # Success message
    print("User Registered Successfully!")

# Run the function
register_user()