""" WebAuth class module.
"""

from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest import AuthService
from .webutils import WebUtils

class WebAuth():
    """ Monostate class responsible of the authentication operation utilities.
    """
    @staticmethod
    def test_token(auth_service: AuthService) -> bool:
        """ Tests whether the session token is valid or not against the authentication service.

        If the token is valid, the session token is updated/refreshed.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - bool: Whether the token is valid (`True`) or not.
        """
        response: ResponseData = auth_service.auth(session.get('token'))
        WebUtils.flash_response_messages(response)
        if not response.is_successful():
            return False

        session['token'] = response.get_content()
        return True
