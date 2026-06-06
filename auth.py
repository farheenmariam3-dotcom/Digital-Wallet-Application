# Import SQLite library
import sqlite3

# Function to login user
def login_user():

    # Ask for username
    username = input("Enter Username: ").strip()

    # Ask for password
    password = input("Enter Password: ")

    # Connect to database
    conn = sqlite3.connect("wallet.db")

    # Create cursor
    cursor = conn.cursor()

    # Find matching username and password
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    # Get matching user
    user = cursor.fetchone()

    # Close database
    conn.close()

    # Check if user exists
    if user:
        print("Login Successful!")
        print("Welcome", username)

    else:
        print("Invalid Username or Password")

# Run login function
login_user()