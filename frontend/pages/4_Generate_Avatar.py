import io
import base64
import streamlit as st
from common_functions import generate_avatar
from PIL import Image


if st.button("Generate Avatar"):
    response = generate_avatar(
        character = "Assassin",
        id_token = st.session_state["auth_id_token"]
    )
    base_64_img_str = response["image"]
    avatar = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))
    
    st.image(avatar, caption='Your Avatar from Stability')