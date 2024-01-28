import streamlit as st

def user_exists(username):
    users = st.secrets["users"]
    return username in users

def sign_up(username, password, additional_info="default_value"):
    users = st.secrets.setdefault("users", {})
    
    if username in users:
        st.warning("Username is already taken. Please choose another one")
    elif username == "":
        st.warning("You have to enter a username")
    elif password == "":
        st.warning("You have to enter a password")
    else:
        user_data = {"password": password, "additional_info": additional_info}
        users[username] = user_data
        st.secrets["users"] = users
        st.success("You have successfully signed up!")

def sign_in(username, password):
    users = st.secrets.get("users", {})
    
    if user_exists(username):
        user_data = users.get(username)    
        if user_data and user_data.get("password") == password:
            additional_info = user_data.get("additional_info", "")
            st.success(f"Welcome, {username}! Additional info: {additional_info}")
            return True
        else:
            st.warning("Incorrect password. Please check for spelling and try again.")
    else:
        st.warning("User does not exist. Please sign up or check the username.")

# Example usage
username_input = st.text_input("Username:")
password_input = st.text_input("Password:", type="password")
if st.button("Sign Up"):
    sign_up(username_input, password_input)

if st.button("Sign In"):
    sign_in(username_input, password_input)
