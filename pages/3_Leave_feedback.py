import streamlit as st
import json
from backend_functions.detect_sentiment import get_response

st.write("This demo takes in feedback from user and performs sentinment analysis using AWS Comprehend")


feedback_text = st.text_area("Leave feedback on your experience")

if st.button("Submit Feedback"):
    # feedback_response = detect_sentiment(feedback_text)
    # st.write(f"You've given {feedback_response['Sentiment']} feedback")

    llm_stream_response = get_response(feedback_text)
    placeholder = st.empty()
    response = ""
    for event in llm_stream_response:
        chunk = json.loads(event['chunk']['bytes'].decode('utf-8'))['completion']
        response += chunk
        placeholder.write(response)