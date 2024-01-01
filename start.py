import streamlit as st
import json
import os
import subprocess

# File path for storing user data
json_file_path = "users.json"
main_script_path = "test.py"

# Function to check if a user exists in the JSON file
def user_exists(username):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            file_contents = file.read()
            if file_contents:
                try:
                    users = json.loads(file_contents)
                except json.JSONDecodeError:
                    st.error("Error decoding JSON. Please check the file format.")
                    return False
            else:
                # If the file is empty, initialize users as an empty dictionary
                users = {}
                with open(json_file_path, "w") as empty_file:
                    json.dump(users, empty_file)
    else:
        users = {}

    return username in users

# Function to sign up a new user
def sign_up(username, password):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            file_contents = file.read()
            if file_contents:
                try:
                    users = json.loads(file_contents)
                except json.JSONDecodeError:
                    st.error("Error decoding JSON. Please check the file format.")
                    return
            else:
                users = {}
    else:
        users = {}

    if username in users:
        st.warning("Username is already taken. Please choose another one.")
    else:
        users[username] = password
        with open(json_file_path, "w") as file:
            json.dump(users, file)
        st.success("You have successfully signed up!")

# Function to sign in a user
def sign_in(username, password):
    if user_exists(username):
        with open(json_file_path, "r") as file:
            users = json.load(file)
            if users.get(username) == password:
                st.success("You have successfully logged in!")

                # Run the main.py script using subprocess
                subprocess.run(["python", main_script_path])
            else:
                st.warning("Incorrect password. Please check for spelling and try again.")
    else:
        st.warning("User does not exist. Please sign up or check the username.")

# Streamlit app
st.title("User Authentication System")

page = st.sidebar.radio("Navigation", ["Home", "Sign Up", "Sign In"])

if page == "Home":
    st.header("Welcome to the User Authentication System!")
elif page == "Sign Up":
    st.header("Sign Up")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Sign Up"):
        sign_up(username, password)
elif page == "Sign In":
    st.header("Sign In")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Sign In"):
        sign_in(username, password)



