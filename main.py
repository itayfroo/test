import streamlit as st
import json
log_check =False
st.title("Sign in page")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'password' not in st.session_state:
    st.session_state.password = ""

def click_button():
    st.session_state.clicked = True

st.button('Sign up', on_click=click_button)

if st.session_state.clicked:
    st.text("Enter your credentials:")
    st.session_state.username = st.text_input("Username:")
    st.session_state.password = st.text_input("Password:", type="password")
    
    if st.button("Sign In"):
        # Check credentials in the 'users.json' file
        with open("users.json", "r") as file:
            users = json.load(file)

        if st.session_state.username in users and users[st.session_state.username] == st.session_state.password:
            st.success("Logged in!")
            log_check =True
        else:
            st.error("Check for username or password mistakes")
