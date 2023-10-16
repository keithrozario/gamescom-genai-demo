import boto3
import json

session = boto3.Session(profile_name='krozario+bedrock-Admin')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

prompt_data = "should I go to the hospital?"
body = json.dumps({"inputText": prompt_data})
modelId = "amazon.titan-embed-text-v1"  # (Change this to try different embedding models)
accept = "application/json"
contentType = "application/json"

response = bedrock_client.invoke_model(
    body=body, modelId=modelId, accept=accept, contentType=contentType
)
response_body = json.loads(response.get("body").read())

embedding = response_body.get("embedding")
print(f"The embedding vector has {len(embedding)} values\n{embedding[0:3 ] +['...' ] +embedding[-3:]}")