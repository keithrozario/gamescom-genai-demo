import json
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
logger = Logger()

@logger.inject_lambda_context
def main(event: dict, context: LambdaContext) -> dict:
    """
    Args:
        event['body']: message to be analyzed
    Returns:
        response: sentiment analysis result
    
    Only accepts English at the moment
    """

    logger.info(event)
    comprehend_client = boto3.client('comprehend')
    message = event['body']
    response = comprehend_client.detect_sentiment(
            Text=message,
            LanguageCode='en'
        )
    logger.info(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

