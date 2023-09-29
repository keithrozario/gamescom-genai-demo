import streamlit as st
from streamlit_player import st_player

from auth_helper import init_cognito_auth
from common_functions import check_user_name

authenticator = init_cognito_auth()

if not authenticator.login():
    st.stop()

def logout():
    authenticator.logout()


with st.sidebar:
    st.text(f"Welcome {st.session_state['auth_username']}")
    st.button("Logout", "logout_btn", on_click=logout)