import streamlit as st

from backend_functions import check_profanity

st.write("This page checks if a username supplied contains a list of banned words")
st.write("Currently, only the words heck, 'heck', 'oi', 'broccoli' are marked as profane")
st.write("We replace usual gamer letter replaces '3'='e' or '$'=s to validate")

handle = st.text_input(label="Enter a username")

if handle:
    profanity_in_user_name = check_profanity.check_banned_words(handle = handle)
    if profanity_in_user_name:
        st.write("This username is already taken, please choose another")
    else:
        st.write("Awesome, your username has been registered. Now let's play")