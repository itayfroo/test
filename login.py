import json
import os
import streamlit as st
import pandas as pd

json_file_path = "users.json"
main_script_path = "test.py"

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
                users = {}
                with open(json_file_path, "w") as empty_file:
                    json.dump(users, empty_file)
    else:
        users = {}
    return username in users


def sign_up(username, password, additional_info="default_value"):
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
        st.warning("Username is already taken. Please choose another one")
    elif username=="":
        st.warning("You have to enter a username")
    elif password=="":
        st.warning("You have to enter a password")
    else:
        user_data = {"username": username,"password": password}
        
        age= st.text_input("Enter your age")
        city= st.text_input("Enter your city name")
        amount_invested= st.text_input("Enter the amount you want to invest")
        
        
        users[username] = user_data
        users[f"{username}_info"] = {'Age':age,'City':city,'Amount_invested':amount_invested}
        with open(json_file_path, "w") as file:
            json.dump(users, file)
        st.success("You have successfully signed up!")



def sign_in(username, password):
    if user_exists(username):
        with open(json_file_path, "r") as file:
            users = json.load(file)
            user_data = users.get(username)    
            if user_data and user_data.get("password") == password:
                additional_info = users.get(f"{username}_info")
                st.success(f"Welcome, {username}! Additional info: {additional_info}")
                d = {
                    'Username': username,
                    'Password': user_data,
                    'Age': f"{username}_info"[0],
                    'City':f"{username}_info"[1],
                    'Amount invested':f"{username}_info"[2]
                }
                df = pd.DataFrame(data=d)
                st.table(df)
                return True
            else:
                st.warning("Incorrect password. Please check for spelling and try again.")
    else:
        st.warning("User does not exist. Please sign up or check the username.")