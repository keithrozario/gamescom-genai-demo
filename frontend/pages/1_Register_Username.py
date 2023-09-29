import streamlit as st

from common_functions import check_user_name

user_name = st.text_input(label="Enter a username")

if user_name:
    profanity_in_user_name = check_user_name(
        user_name = user_name,
        id_token = st.session_state["auth_id_token"]
    )
    if profanity_in_user_name:
        st.write("This username is already taken, please choose another")
    else:
        st.write("Awesome, your username has been registered. Now let's play")