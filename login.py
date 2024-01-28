import sqlite3
import streamlit as st
import hashlib

# Function to create a connection and cursor to the SQLite database
def create_connection():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    return conn, cursor

# Function to create the users table if it doesn't exist
def create_users_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            additional_info TEXT
        )
    ''')

# Function to sign up a new user
def sign_up(username, password, additional_info="default_value"):
    conn, cursor = create_connection()

    try:
        # Check if the user already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.warning("Username is already taken. Please choose another one.")
        elif username == "" or password == "":
            st.warning("Please enter a username and password.")
        else:
            # Hash the password before storing it
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Insert the new user into the database
            cursor.execute('''
                INSERT INTO users (username, password, additional_info)
                VALUES (?, ?, ?)
            ''', (username, hashed_password, additional_info))
            conn.commit()
            st.success("You have successfully signed up!")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

# Function to sign in an existing user
def sign_in(username, password):
    conn, cursor = create_connection()

    try:
        # Hash the entered password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username and hashed password match
        cursor.execute('''
            SELECT * FROM users
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))

        user_data = cursor.fetchone()

        if user_data:
            st.success(f"Welcome, {username}! Additional info: {user_data[2]}")
        else:
            st.warning("Incorrect username or password. Please try again.")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

# Streamlit UI
st.title("User Authentication with SQLite")

# Sign-up section
st.header("Sign Up")
new_username = st.text_input("Enter a new username:")
new_password = st.text_input("Enter a new password:", type="password")
additional_info = st.text_input("Enter additional info (optional):")
if st.button("Sign Up"):
    sign_up(new_username, new_password, additional_info)

# Sign-in section
st.header("Sign In")
existing_username = st.text_input("Enter your username:")
existing_password = st.text_input("Enter your password:", type="password")
if st.button("Sign In"):
    sign_in(existing_username, existing_password)
