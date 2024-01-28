import json
import os
import streamlit as st
import pandas as pd
import numpy as np
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
        user_data = {"password": password}
        
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
                audio_file = open('myaudio.ogg', 'rb')
                audio_bytes = audio_file.read()

                st.audio(audio_bytes, format='audio/ogg')

                sample_rate = 44100  # 44100 samples per second
                seconds = 2  # Note duration of 2 seconds
                frequency_la = 440  # Our played note will be 440 Hz
                # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
                t = np.linspace(0, seconds, seconds * sample_rate, False)
                # Generate a 440 Hz sine wave
                note_la = np.sin(frequency_la * t * 2 * np.pi)

                st.audio(note_la)
               
                d = {
                    'Username': username,
                    'Password': user_data,
                    'Age': additional_info['Age'],
                    'City':additional_info['City'],
                    'Amount invested':additional_info['Amount_invested']
                }
                df = pd.DataFrame([d])
                st.table(df)
                return True
            else:
                st.warning("Incorrect password. Please check for spelling and try again.")
    else:
        st.warning("User does not exist. Please sign up or check the username.")