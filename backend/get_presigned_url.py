from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from datetime import datetime
import os
import json

logger = Logger()
s3_client = boto3.client('s3')

@logger.inject_lambda_context
def main(event: dict, context: LambdaContext) -> dict:

    logger.info(event)
    user_name = event['requestContext']['authorizer']['claims']['cognito:username']
    
    now = datetime.utcnow()
    s3_key = f"{user_name}/{now.year}-{now.month}/{now.isoformat()}.zip"

    presigned_post_url = s3_client.generate_presigned_post(
        Bucket = os.environ['S3_BUCKET_NAME'],
        Key = s3_key,
        ExpiresIn=120
    )
    return {
        "statusCode": 200,
        "body": json.dumps(presigned_post_url)
    }