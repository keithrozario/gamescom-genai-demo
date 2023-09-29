import json
import boto3
import random

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
logger = Logger()

session = boto3.Session()
bedrock_client = session.client(service_name='bedrock-runtime', region_name='us-west-2')
s3_client = session.client(service_name='s3', region_name='us-west-2')

@logger.inject_lambda_context
def main(event: dict, context: LambdaContext) -> dict:
    """
    Args:
        event['character']: character to be drawn (e.g. 'Assassin', 'Wizard', 'Orc')
    returns:
        image: base64 representation of image
    """

    character = "The headshot of a futuristic assasin, drawn as a woman, wearing black sunglasses. Drawn as an Avatar for computer game"
    neg_prompt = "face"

    request = json.dumps({
        "text_prompts": (
            [
                {"text": character, "weight": 2.0},
                {"text": neg_prompt, "weight": -1.0}
            ]
        ),
        "cfg_scale": 28,
        "seed": random.randint(1, 4294967295),
        "steps": 10
    })
    modelId = "stability.stable-diffusion-xl-v0"

    response = bedrock_client.invoke_model(
        body=request,
        modelId=modelId,
        contentType= "application/json",
        accept= "application/json",
    )
    logger.info(response)
    response_body = json.loads(response.get("body").read())
    base_64_img_str = response_body["artifacts"][0].get("base64")
    return_object = {
        "image": base_64_img_str
    }
    logger.info(return_object)
    
    return {
        'statusCode': 200,
        'body': json.dumps(return_object)
    }

    # response_image = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))
    # response_image.save(f"/tmp/{character}.png")