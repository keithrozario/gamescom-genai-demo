import json
import boto3
import random

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
logger = Logger()

session = boto3.Session()
bedrock_client = session.client(service_name='bedrock-runtime', region_name='us-west-2')

@logger.inject_lambda_context
def main(event: dict, context: LambdaContext) -> dict:
    """
    Generates an avatar from the character

    Args:
        event['character_option']: character to generate the avatar from
        event['character_era']: character era to generate the avatar from
        event['character_gender']: character gender to generate the avatar from
        event['character_features']: character features to generate the avatar from
    Returns:
        response: JSON object, which has base64 'image' of response 
    """
    logger.info(event)

    request = json.loads(event['body'])

    era = request['character_era']
    character_option = request['character_option']
    gender = request['character_gender']
    added_features = add_features(era, character_option, gender)

    character = f"The headshot of a {era} {character_option}, drawn as a {gender}. Drawn as an Avatar for computer game"
    logger.info({"Prompt": character})

    text_prompts = [
                {"text": character, "weight": 2.0}
            ]
    text_prompts.extend(added_features)

    request = json.dumps({
        "text_prompts": (
            [
                {"text": character, "weight": 2.0},
                {"text": added_features, "weight": 1.5}
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
    logger.debug(response)

    response_body = json.loads(response.get("body").read())
    base_64_img_str = response_body["artifacts"][0].get("base64")
    return_object = {
        "image": base_64_img_str,
        "prompt": character,
    }
    logger.debug(return_object)
    
    return {
        'statusCode': 200,
        'body': json.dumps(return_object)
    }

def add_features(era, character_option, gender):
    """
    Adds features to the character

    Args:
        era: character era
        character_option: character option
        gender: character gender
    Returns:
        features: list of features
    """
    features = []

    if era == "Steampunk":
        features.append({"text": "Steampunk Goggles", "weight": 1.5})
    if character_option == "Android":
        features.append({"text": "Grey Skin", "weight": 1.5}, {"text": "Screws", "weight": 1.5})
    if character_option == "Wizard":
        features.append({"text": "Grey Hair", "weight": 1.5}, {"text": "Magic", "weight": 1.5})
    if era == "Medieval":
        features.append({"text": "Medival Armor", "weight": 1.5}, {"text": "Medival Sword", "weight": 1.5})  

    return features