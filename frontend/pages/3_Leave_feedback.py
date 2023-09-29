import streamlit as st
from common_functions import submit_feedback

feedback_text = st.text_area("Leave feedback on your experience")
if st.button("Submit Feedback"):
    feedback_response = submit_feedback(
        feedback_text = feedback_text,
        id_token = st.session_state["auth_id_token"]
    )
    st.write(f"You've given {feedback_response['Sentiment']} feedback")