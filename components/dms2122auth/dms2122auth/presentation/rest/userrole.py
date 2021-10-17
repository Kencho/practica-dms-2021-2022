""" REST API controllers responsible of handling the role operations.
"""

from typing import Dict, Tuple, List, Optional, Union
from http import HTTPStatus
from flask import current_app
from dms2122auth.data.db.exc import UserNotFoundError
from dms2122auth.service import RoleServices
from dms2122common.data import Role


def user_has_role(username: str, rolename: str) -> Tuple[Optional[str], Optional[int]]:
    """Determine whether a user has a role.

    Args:
        - username (str): The user name.
        - rolename (str): The role name.

    Returns:
        - Tuple[Optional[str], Optional[int]]: A tuple with no content and codes:
            - 200 if the user has the role.
            - 404 if the user does not have the role.
    """
    with current_app.app_context():
        has_role: bool = RoleServices.has_role(
            username, rolename, current_app.db)
        if has_role:
            return (None, HTTPStatus.OK.value)
    return (None, HTTPStatus.NOT_FOUND.value)


def list_user_roles(username: str, token_info: Dict) -> Tuple[Union[List[str], str], Optional[int]]:
    """Lists the roles of a user.

    Args:
        - username (str): The user name.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[List[str], str], Optional[int]]: A tuple with the list of user roles and a
          code 200 OK on success. Otherwise, a description message and codes:
            - 400 BAD REQUEST if the username is missing.
            - 403 FORBIDDEN if the requesting user has no rights to list the roles.
    """
    with current_app.app_context():
        if (not RoleServices.has_role(token_info['user_token']['user'], Role.Admin, current_app.db)
                and username != token_info['user_token']['user']):
            return (
                'Current user has not enough privileges to view other users\' roles',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            user_roles: List[str] = RoleServices.list_user_roles(
                username, current_app.db)
        except ValueError:
            return ("No username given.", HTTPStatus.BAD_REQUEST.value)
        return (user_roles, HTTPStatus.OK.value)


def grant_role(
    username: str, rolename: str, token_info: Dict
) -> Tuple[Optional[str], Optional[int]]:
    """Grants a role to a user.

    Args:
        - username (str): The user name.
        - rolename (str): The role name.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Optional[str], Optional[int]]: A tuple of no content and code 200 OK if granted, or
          a description message and codes:
            - 400 BAD REQUEST if a mandatory parameter is missing.
            - 403 FORBIDDEN if the requesting user has no rights to grant a role.
            - 404 NOT FOUND if the user does not exist.
    """
    with current_app.app_context():
        if not RoleServices.has_role(token_info['user_token']['user'], Role.Admin, current_app.db):
            return (
                'Current user has not enough privileges to grant roles',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            RoleServices.grant_role(username, rolename, current_app.db)
        except ValueError:
            return (
                'Both a username and a role name must be given',
                HTTPStatus.BAD_REQUEST.value
            )
        except UserNotFoundError:
            return (f'User {username} was not found', HTTPStatus.NOT_FOUND.value)
        return (None, HTTPStatus.OK.value)


def revoke_role(
    username: str, rolename: str, token_info: Dict
) -> Tuple[Optional[str], Optional[int]]:
    """Revokes a role from a user.

    Args:
        - username (str): The user name.
        - rolename (str): The role name.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Optional[str], Optional[int]]: A tuple of no content and code 200 OK if revoked, or
          a description message and codes:
            - 400 BAD REQUEST if a mandatory parameter is missing.
            - 403 FORBIDDEN if the requesting user has no rights to revoke a role.
    """
    with current_app.app_context():
        if not RoleServices.has_role(token_info['user_token']['user'], Role.Admin, current_app.db):
            return (
                'Current user has not enough privileges to revoke roles',
                HTTPStatus.FORBIDDEN.value
            )
        if token_info['user_token']['user'] == username and Role[rolename] is Role.Admin:
            return (
                'Current user cannot revoke the Admin role from oneself',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            RoleServices.revoke_role(username, rolename, current_app.db)
        except ValueError:
            return 'Both a username and a role name must be given', HTTPStatus.BAD_REQUEST.value
        return (None, HTTPStatus.OK.value)
