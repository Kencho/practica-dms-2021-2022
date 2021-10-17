""" REST API controllers responsible of handling the user operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from flask import current_app
from dms2122auth.data.db.exc import UserExistsError
from dms2122auth.service import UserServices, RoleServices
from dms2122common.data.role import Role


def list_users() -> Tuple[List[Dict], Optional[int]]:
    """Lists the existing users.

    Returns:
        - Tuple[List[Dict], Optional[int]]: A tuple with a list of dictionaries for the users' data
          and a code 200 OK.
    """
    with current_app.app_context():
        users: List[Dict] = UserServices.list_users(current_app.db)
    return (users, HTTPStatus.OK.value)


def create_user(body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Creates a user if the requestor has the Admin role.

    Args:
        - body (Dict): A dictionary with the new user's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new user data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the user.
            - 409 CONFLICT if an existing user already has all or part of the unique user's data.
    """
    with current_app.app_context():
        if not RoleServices.has_role(token_info['user_token']['user'], Role.Admin, current_app.db):
            return (
                'Current user has not enough privileges to create a user',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            user: Dict = UserServices.create_user(
                body['username'], body['password'], current_app.db, current_app.cfg
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except UserExistsError:
            return ('A user with the given username already exists', HTTPStatus.CONFLICT.value)
    return (user, HTTPStatus.OK.value)
