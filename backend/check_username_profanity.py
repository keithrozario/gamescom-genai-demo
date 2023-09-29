"""
Function checks a username for profanity, defined in the list of banned words.
Username will be turned into canonical form (lowercase, no punctuation, convert 3=>e, 5=>s and so forth).
"""

import json

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

conversions = [
    ('0', 'o'),
    ('1', 'i'),
    ('2', 'z'),
    ('3', 'e'),
    ('4', 'a'),
    ('5', 's'),
    ('6', 'b'),
    ('7', 't'),
    ('8', 'b'),
    ('9', 'g'),
    ('!', 'i'),
    ('@', 'a'),
    ('$', 's'),
    ('&', 'b'),
    ('_', ' '),
    ('-', ' '),
    ('.', ' '),
    (',', ' '),
    ('?', ' '),
    ('*', ' ')
]

banned_words = ['heck', 'oi', 'brussel sprouts']

@logger.inject_lambda_context
def main(event: dict, context: LambdaContext) -> dict:
    """
    Args:
        event['user_name'] (str): User name to check, as entered by user
    return:
        profanity_present (bool): Boolean of if username has profanity or not.
    """
    logger.info(event)

    user_name = event['queryStringParameters']['user_name']

    canonical_user_name = reduce_to_canonical(user_name)
    logger.info(canonical_user_name)
    profanity_present = check_profanity(canonical_user_name)
    logger.info(profanity_present)

    return {
        "statusCode": 200,
        "body": json.dumps({
            'user_name': user_name,
            'profanity_present': profanity_present
    })
    }


def reduce_to_canonical(username: str) -> str:
    """
    Args:
        username (str): User name to check
    return:
        username (str): User name in canonical form
    """

    for conversion in conversions:
        username = username.replace(conversion[0], conversion[1])
    username = username.lower()
    return username


def check_profanity(canonical_user_name: str) -> bool:
    """
    Args:
        canonical_username (str): User name in canonical form
    return:
        response (bool): Boolean of if username is acceptable or not. True if acceptable, False if not.
    """
    response = False

    # Username can have multiple words
    for word in canonical_user_name.split(' '):
        if word in banned_words:
            response = True

    return response