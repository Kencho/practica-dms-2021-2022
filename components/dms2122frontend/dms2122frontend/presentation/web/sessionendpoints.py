""" SessionEndpoints class module.
"""

from typing import Text, Union
from flask import request, redirect, url_for, render_template, session, flash
from werkzeug.wrappers import Response
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest import AuthService
from .webauth import WebAuth
from .webuser import WebUser
from .webutils import WebUtils


class SessionEndpoints():
    """ Monostate class responsible of handling the session web endpoint requests.
    """
    @staticmethod
    def get_login(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the login endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if WebAuth.test_token(auth_service):
            return redirect(url_for('get_home'))
        return render_template('login.html')

    @staticmethod
    def post_login(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the login endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        response: ResponseData = auth_service.login(
            request.form['user'], request.form['pass'])
        WebUtils.flash_response_messages(response)
        if not response.is_successful():
            return redirect(url_for('get_login'))

        session['user'] = request.form['user']
        session['token'] = response.get_content()
        session['roles'] = WebUser.get_roles(auth_service, session['user'])
        return redirect(url_for('get_home'))

    @staticmethod
    def get_logout() -> Union[Response, Text]:
        """ Handles the GET requests to the logout endpoint.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        session.clear()
        flash('Session closed', 'info')
        return redirect(url_for('get_login'))
