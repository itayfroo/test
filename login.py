import sqlite3
import streamlit as st

db_path = "users.db"

def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            additional_info TEXT
        )
    ''')

    conn.commit()
    conn.close()

def user_exists(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    return user is not None

def sign_up(username, password, additional_info="default_value"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if user_exists(username):
        st.warning("Username is already taken. Please choose another one.")
    elif username == "":
        st.warning("You have to enter a username.")
    elif password == "":
        st.warning("You have to enter a password.")
    else:
        cursor.execute('''
            INSERT INTO users (username, password, additional_info)
            VALUES (?, ?, ?)
        ''', (username, password, additional_info))

        conn.commit()
        conn.close()
        st.success("You have successfully signed up!")

def sign_in(username, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        st.success(f"Welcome, {username}! Additional info: {user[2]}")
        return True
    else:
        st.warning("Incorrect password. Please check for spelling and try again.")
        return False

initialize_database()
