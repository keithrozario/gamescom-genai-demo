import io
import base64
import json
import boto3
import random
from PIL import Image


boto3_session = boto3.Session(profile_name='krozario+bedrock-Admin')
bedrock_client = boto3_session.client(service_name='bedrock-runtime', region_name='us-west-2')

# Orc
# character = "The headshot of a scary looking green Orc Warrior. Grinning and smiling. Drawn as an Avatar for computer game"
# neg_prompt = "pointed ears"

# Wizard
# character = "The headshot of a Wise Wizard with Grey Hair and Long Beard wearing white. Drawn as an Avatar for computer game"
# neg_prompt = "moustache"

# Steampunk Warrior
# character = "The headshot of a Steampunk engineer, with thick Goggles and a crazy smile. Drawn as an Avatar for computer game"
# neg_prompt = "bald"

# # Knight
# character = "The headshot of a Battle Knight, wearing a medival coat of armor. Drawn as an Avatar for computer game"
# neg_prompt = "face"

# Assassin
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
response_body = json.loads(response.get("body").read())
base_64_img_str = response_body["artifacts"][0].get("base64")
response_image = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))
response_image.save(f"{character}.png")

print(response)