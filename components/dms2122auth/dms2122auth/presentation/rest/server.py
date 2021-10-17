""" REST API controllers responsible of handling the server operations.
"""

from typing import Dict, Tuple, Optional
from http import HTTPStatus
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer


def health_test() -> Tuple[None, Optional[int]]:
    """Simple health test endpoint.

    Returns:
        - Tuple[None, Optional[int]]: A tuple of no content and code 204 No Content.
    """
    return (None, HTTPStatus.NO_CONTENT.value)


def login(token_info: Dict) -> Tuple[str, Optional[int]]:
    """Generates a user token if the user validation was passed.

    Args:
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[str, Optional[int]]: A tuple with the JWS token and code 200 OK.
    """
    with current_app.app_context():
        jws: TimedJSONWebSignatureSerializer = current_app.jws
        user: str = ''
        if 'user_token' in token_info:
            user = token_info['user_token']['user']
        elif 'user_credentials' in token_info:
            user = token_info['user_credentials']['user']
        token = jws.dumps({
            'user': user,
            'sub': user
        })
        return (token.decode('ascii'), HTTPStatus.OK.value)
