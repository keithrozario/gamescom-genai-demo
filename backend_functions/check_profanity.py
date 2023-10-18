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

banned_words = ['heck', 'oi', 'broccoli']

def check_banned_words(handle: str) -> bool:
    """
    Args:
        handle (str): User name to check, as entered by user
    return:
        profanity_present (bool): Boolean of if username has profanity or not.
        For the purpose of this demo, only the 3 words are considered profanity.
    """

    canonical_user_name = reduce_to_canonical(handle)
    profanity_present = check_profanity(canonical_user_name)

    return profanity_present


def reduce_to_canonical(username: str) -> str:
    """
    Args:
        username (str): User name to check
    return:
        username (str): User name in canonical form
    """

    username = username.lower()
    for conversion in conversions:
        username = username.replace(conversion[0], conversion[1])
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