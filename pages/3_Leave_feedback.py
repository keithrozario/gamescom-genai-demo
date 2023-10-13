import streamlit as st
from common_functions import submit_feedback


st.write("This demo takes in feedback from user and performs sentinment analysis using AWS Comprehend")


feedback_text = st.text_area("Leave feedback on your experience")
if st.button("Submit Feedback"):
    feedback_response = submit_feedback(
        feedback_text = feedback_text,
        id_token = "null"
    )
    st.write(f"You've given {feedback_response['Sentiment']} feedback")