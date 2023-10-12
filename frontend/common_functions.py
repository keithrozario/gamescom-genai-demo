import json
import io
import zipfile
import requests
import streamlit as st

api_domain = "https://r47yjn6a2i.execute-api.us-west-2.amazonaws.com/dev"

def check_user_name(user_name: str):
    """
    Checks if the username has profanity

    Args:
        username: username to check
    Returns:
        profanity_present: Boolean response if profanity is in user_name
    """
    
    response = requests.get(
        url = f"{api_domain}/check-username-profanity",
        params = {"user_name": user_name}
    ).content.decode('utf-8')

    response_dict = json.loads(response)
    profanity_present = response_dict["profanity_present"]

    return profanity_present


def submit_feedback(feedback_text: str):
    """
    Submits feedback to the API Gateway

    Args:
        feedback_text: feedback text to submit
        id_token: id token to call the API Gateway with
    Returns:
        response: JSON response in string format
    """
    response = requests.post(
        url = f"{api_domain}/detect-sentiment",
        json = {"feedback_text": feedback_text}
    ).content.decode('utf-8')

    response_dict = json.loads(response)
    
    return response_dict
