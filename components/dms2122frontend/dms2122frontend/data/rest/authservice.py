""" AuthService class module.
"""

from typing import List, Optional, Union
import requests
from dms2122common.data import Role
from dms2122common.data.rest import ResponseData


class AuthService():
    """ REST client to connect to the authentication service.
    """

    def __init__(self,
                 host: str, port: int,
                 api_base_path: str = '/api/v1',
                 apikey_header: str = 'X-ApiKey-Auth',
                 apikey_secret: str = ''
                 ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The authentication service host string.
            - port (int): The authentication service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret

    def __base_url(self) -> str:
        """ Constructs the base URL for the requests.

        Returns:
            - str: The base URL.
        """
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def login(self, username: str, password: str) -> ResponseData:
        """ Performs a login request to the authentication service.

        Args:
            - username (str): The username.
            - password (str): The password.

        Returns:
            - ResponseData: If successful, the contents hold a string with the user session token.
        """
        response: requests.Response = requests.post(
            self.__base_url() + '/auth',
            auth=(username, password),
            headers={
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data: ResponseData = ResponseData()
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.content.decode('ascii'))
        else:
            response_data.add_message('Invalid credentials')
        return response_data

    def auth(self, token: Optional[str]) -> ResponseData:
        """ Performs an authentication request to the authentication service.

        Args:
            - token (Optional[str]): The user session token to validate.

        Returns:
            - ResponseData: If successful, the contents hold a string with a new user session token.
              Otherwise, the session is rejected (e.g., timed out, was invalidated, was missing)
        """
        response_data: ResponseData = ResponseData()
        if not token:
            response_data.set_successful(False)
            return response_data

        response: requests.Response = requests.post(
            self.__base_url() + '/auth',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.content.decode('ascii'))
        else:
            response_data.add_message('Session expired')
        return response_data

    def list_users(self, token: Optional[str]) -> ResponseData:
        """ Requests a list of registered users.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of user data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/users',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def create_user(self, token: Optional[str], username: str, password: str) -> ResponseData:
        """ Requests a user creation.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The new user's name.
            - password (str): The new user's password.

        Returns:
            - ResponseData: If successful, the contents hold the new user's data.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + '/user/new',
            json={
                'username': username,
                'password': password
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_user_roles(self, token: Optional[str], username: str) -> ResponseData:
        """ Requests the list of roles assigned to a user.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The name of the queried user.

        Returns:
            - ResponseData: If successful, the contents hold a list of role names. Otherwise an
              empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/user/{username}/roles',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def grant_user_role(self,
                        token: Optional[str], username: str, role: Union[Role, str]
                        ) -> ResponseData:
        """ Requests to grant a role to a user.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The user to be granted the role.
            - role (Union[Role, str]): The role to be granted.

        Returns:
            - ResponseData: Useful to know whether the operation succeeded and its messages.
        """
        if isinstance(role, Role):
            role = role.name
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/user/{username}/role/{role}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if not response_data.is_successful():
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def revoke_user_role(self,
                         token: Optional[str], username: str, role: Union[Role, str]
                         ) -> ResponseData:
        """ Requests to revoke a role from a user.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The user to be revoked the role.
            - role (Union[Role, str]): The role to be revoked.

        Returns:
            - ResponseData: Useful to know whether the operation succeeded and its messages.
        """
        if isinstance(role, Role):
            role = role.name
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.delete(
            self.__base_url() + f'/user/{username}/role/{role}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if not response_data.is_successful():
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def update_user_roles(self,
                          token: Optional[str], username: str, new_roles: List
                          ) -> ResponseData:
        """ Requests to update several roles on a user at once.

        This is an utility method. If at least one of them fails, all of them are considered failed,
        though some of the changes may have taken effect. The messages should describe the failure
        reasons.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The user to have their roles updated.
            - new_roles (List): A list of roles to update. If present in the list, will be granted;
              otherwise, they will be revoked.

        Returns:
            - ResponseData: Useful to know whether the operation succeeded and its messages.
        """
        aggregated_response: ResponseData = ResponseData()
        aggregated_response.set_successful(True)
        for role in Role:
            response: ResponseData
            if role.name in new_roles:
                response = self.grant_user_role(token, username, role)
            else:
                response = self.revoke_user_role(token, username, role)
            aggregated_response.add_messages(response.get_messages())
            aggregated_response.set_successful(
                aggregated_response.is_successful() & response.is_successful())
        return aggregated_response
