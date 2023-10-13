import json
import boto3
import random
from PIL import Image
import io
import base64

session = boto3.Session()
bedrock_client = session.client(service_name='bedrock-runtime', region_name='us-west-2')

def generate_avatar(character_era: str, character_option: str, character_gender:str) -> Image:
    """
    Generate a Stability-AI Avatar based on the user's input.
    :param character_era: The era of the character.
    :param character_option: The type of character.
    :param character_gender: The gender of the character.
    :return: The avatar as an Image object.
    """
    
    prompt = f"The headshot of a {character_era} {character_option}, drawn as a {character_gender}. Drawn as an Avatar for computer game"
    request = json.dumps({
        "text_prompts": (
            [
                {"text": prompt, "weight": 2.0}
            ]
        ),
        "cfg_scale": 28,
        "seed": random.randint(1, 4294967295),
        "steps": 80
    })
    modelId = "stability.stable-diffusion-xl-v0"

    response = bedrock_client.invoke_model(
        body=request,
        modelId=modelId,
        contentType= "application/json",
        accept= "application/json",
    )
    response_body = json.loads(response.get("body").read())
    base_64_img_str = response_body["artifacts"][0].get("base64")
    avatar = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))
    
    return avatar