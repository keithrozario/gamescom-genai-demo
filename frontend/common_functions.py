import json
import io
import zipfile
import requests
import streamlit as st

api_domain = "https://r47yjn6a2i.execute-api.us-west-2.amazonaws.com/dev"

def upload_to_s3(presigned_response: str, picture):
    """
    Uploads the picture from the camera to the presigned URL in s3. 
    Zips the picture before uploading (prior versions before zipping didn't work)

    Args:
        presigned_respose: JSON response from the presigned post request
        picture: output of the st.camera_input
    Returns:
        status_code: Status code of the upload
    """

    presigned_post_data = json.loads(presigned_response)
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w') as fileobj:

        fileobj.writestr(
            zinfo_or_arcname='image.jpeg',
            data=picture.getbuffer()
        )
    memory_file.seek(0)
    files = {'file': ('file.zip', memory_file, '')}
    
    http_response = requests.post(
        url=f"{presigned_post_data['url']}", 
        data=presigned_post_data['fields'],
        files=files
    )

    return http_response.status_code


def get_presigned_post_url(id_token: str):
    """
    Gets presigned post url to post to S3 from

    Args:
        id_token: id token to call the API Gateway with
    Returns:
        response: JSON response in string format
    """
    response = requests.get(
        url=f"{api_domain}/presigned-url",
        headers={"Authorization": id_token}
    ).content.decode('utf-8')

    return response


def check_user_name(user_name: str, id_token: str):
    """
    Checks if the username has profanity

    Args:
        username: username to check
    Returns:
        profanity_present: Boolean response if profanity is in user_name
    """
    
    response = requests.get(
        url = f"{api_domain}/check-username-profanity",
        headers = {"Authorization": id_token},
        params = {"user_name": user_name}
    ).content.decode('utf-8')

    response_dict = json.loads(response)
    profanity_present = response_dict["profanity_present"]

    return profanity_present


def submit_feedback(feedback_text: str, id_token: str):
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
        headers = {"Authorization": id_token},
        json = {"feedback_text": feedback_text}
    ).content.decode('utf-8')

    response_dict = json.loads(response)
    
    return response_dict


def generate_avatar(character: str, id_token: str):
    """
    Generates an avatar from the character

    Args:
        character: character to generate the avatar from
    Returns:
        response: JSON response in string format, which has base64 'image' of response 
    """

    response = requests.post(
        url = f"{api_domain}/generate-avatar",
        headers = {"Authorization": id_token},
        json = {"character": character}
    ).content.decode('utf-8')

    response_dict = json.loads(response)
    
    return response_dict
