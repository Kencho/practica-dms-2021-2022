""" CommonEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template
from werkzeug.wrappers import Response
from dms2122frontend.data.rest.authservice import AuthService
from .webauth import WebAuth


class CommonEndpoints():
    """ Monostate class responsible of handling the common web endpoint requests.
    """
    @staticmethod
    def get_home(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the home endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        name = session['user']
        return render_template('home.html', name=name, roles=session['roles'])
