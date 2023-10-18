import streamlit as st
import json
from backend_functions.detect_sentiment import detect_sentiment, get_response

st.write("This demo takes in feedback from user and performs sentinment analysis using AWS Comprehend, and after that generates a response to user using an LLM. The prompts for NEGATIVE or POSITIVE feedbacks are different")


feedback_text = st.text_area("Leave feedback on your experience")

if st.button("Submit Feedback"):
    feedback_response = detect_sentiment(feedback_text)
    sentiment = feedback_response['Sentiment']
    st.write(f"You've given {sentiment} feedback")

    llm_stream_response = get_response(feedback_text, sentiment)
    placeholder = st.empty()
    response = ""
    for event in llm_stream_response:
        chunk = json.loads(event['chunk']['bytes'].decode('utf-8'))['completion']
        response += chunk
        placeholder.write(response)

