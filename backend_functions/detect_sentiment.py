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


def get_response(feedback: str, sentiment: str) -> str:
    """
    Args:
        event['body']: Message to be analyzed
    Returns:
        body['message']: Feedback from the Titan model    
    """
   
    bedrock_client = boto3.client('bedrock-runtime')
    bedrock_model_id = "anthropic.claude-v2"
  
    if sentiment == "NEGATIVE":

        prompt = f"Human: \
        You are a polite customer service agent for a company that makes mobile games. \
        A customer has just made a complaint, please provide a response that addresses each point in the complaint promising that we will improve. \
        At the end apologize for the issues caused. \
        Here is the customers statement. \
        '{feedback}' \n\n \
        Assistant:"
    
    else:

        prompt = f"Human: \
        You are a polite customer service agent for a company that makes mobile games. \
        A customer has just provided  feedback, please provide a response that addresses any specific points in the feedback. \
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
