import streamlit as st

from common_functions import check_user_name

user_name = st.text_input(label="Enter a username")

st.write("This page checks if a username supplied contains profanity")
st.write("Currently, only the words heck, 'heck', 'oi', 'brussel sprouts' are marked as profane")
st.write("We replace usual gamer letter replaces '3'='e' or '$'=s to validate")

if user_name:
    profanity_in_user_name = check_user_name(
        user_name = user_name,
        id_token = "null"
    )
    if profanity_in_user_name:
        st.write("This username is already taken, please choose another")
    else:
        st.write("Awesome, your username has been registered. Now let's play")