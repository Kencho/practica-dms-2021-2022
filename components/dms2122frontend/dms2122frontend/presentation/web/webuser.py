""" WebUser class module.
"""

from typing import Dict, List, Optional
from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest.authservice import AuthService
from .webutils import WebUtils


class WebUser():
    """ Monostate class responsible of the user operation utilities.
    """
    @staticmethod
    def list_users(auth_service: AuthService) -> List:
        """ Gets the list of users from the authentication service.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - List: A list of user data dictionaries (the list may be empty)
        """
        response: ResponseData = auth_service.list_users(session.get('token'))
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []

    @staticmethod
    def create_user(auth_service: AuthService, username: str, password: str) -> Optional[Dict]:
        """ Creates a user in the authentication service.

        Args:
            - auth_service (AuthService): The authentication service.
            - username (str): The name of the user to be created.
            - password (str): The password of the user to be created.

        Returns:
            - Dict: A dictionary with the newly created user if successful.
            - None: Nothing on error.
        """
        response: ResponseData = auth_service.create_user(
            session.get('token'), username, password)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def get_roles(auth_service: AuthService, username: str) -> List:
        """ Gets the list of roles granted to a user from the authentication service.

        Args:
            - auth_service (AuthService): The authentication service.
            - username (str): The name of the queried user.

        Returns:
            - List: A list of role names on success. On error, the list will be empty.
        """
        response: ResponseData = auth_service.get_user_roles(
            session.get('token'), username)
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []

    @staticmethod
    def update_user_roles(auth_service: AuthService, username: str, roles: List) -> bool:
        """ Updates the user roles in the authentication service.

        Args:
            - auth_service (AuthService): The authentication service.
            - username (str): The user with the roles updated.
            - roles (List): The list of roles to grant. Roles not present here will be revoked.

        Returns:
            - bool: Whether all the roles were updated successfully (`True`) or there were some
              errors (`False`)
        """
        response: ResponseData = auth_service.update_user_roles(
            session.get('token'), username, roles)
        WebUtils.flash_response_messages(response)
        return response.is_successful()
