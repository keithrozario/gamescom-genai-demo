import boto3
import json

def detect_sentiment(message: str) -> dict:
    """
    Args:
        message: message to be analyzed
    Returns:
        response: sentiment analysis result
    
    Only accepts English at the moment
    """
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_sentiment(
            Text=message,
            LanguageCode='en'
        )
    
    return response


def get_response(feedback: str) -> str:
    """
    Args:
        event['body']: Message to be analyzed
    Returns:
        body['message']: Feedback from the Titan model    
    """
   
    bedrock_client = boto3.client('bedrock-runtime')
    bedrock_model_id = "anthropic.claude-v2"
  
    prompt = f"Human: \
    You are a polite customer service agent for a company that makes mobile games. \
    A customer has just provided the feedback below, please provide a response that addresses complaint in the feedback. \
    If the customer complains about the game being laggy, mention that there is a known issue on iOS version 12.0.1 that might be responsible. \
    Here is the customers statement. \
    '{feedback}' \n\n \
    Assistant:"

    body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample":4096,
            "temperature":0.5,
            "top_k":250,
            "top_p":0.5,
            "stop_sequences":[]
        })

    response = bedrock_client.invoke_model_with_response_stream(
        body=body,
        modelId=bedrock_model_id, 
        accept='*/*',
        contentType='application/json'
    ) 
    

    stream = response.get('body')
    return stream
