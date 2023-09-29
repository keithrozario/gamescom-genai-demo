import json
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
logger = Logger()


session = boto3.Session()
bedrock_client = session.client(
    service_name='bedrock',
    region_name="us-west-2",
    endpoint_url="https://prod.us-west-2.frontend.bedrock.aws.dev"
)


@logger.inject_lambda_context
def main(event: dict, context: LambdaContext) -> dict:
    """
    Args:
        event['body']: Message to be analyzed
    Returns:
        body['message']: Feedback from the Titan model    
    """

    bedrock_model_id = "amazon.titan-tg1-large"

    customer_feedback = event['body']
    
    prompt = f"You are a polite customer service agent for a company that makes mobile games. \
    A customer has just provided the feedback below, please provide a response that addresses complaint or compliment in the feedback. \
    If the customer complains about being laggy, mention that there is a known issue on iOS version 12.0.1 that might be responsible, if not do not mention this. \
    Here is the customers statement. '{customer_feedback}'"

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "stopSequences": [],
            "temperature": 0,
            "topP": 0.9 } } )

    response = bedrock_client.invoke_model(
        body=body,
        modelId=bedrock_model_id, 
        accept='application/json',
        contentType='application/json'
    ) 
        
    response_body = json.loads(response.get('body').read())
    logger.info(response_body)
    response_text = response_body.get('results')[0].get('outputText')
    
    return {
        'statusCode': 200,
        'body': {
            "response": response_text
        }
    }