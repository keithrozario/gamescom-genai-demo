import streamlit as st

st.write("Placeholder page for game play")
video_file = open('./assets/video.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)