""" TeacherEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from .webauth import WebAuth


class TeacherEndpoints():
    """ Monostate class responsible of handing the teacher web endpoint requests.
    """
    @staticmethod
    def get_teacher(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the teacher root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('teacher.html', name=name, roles=session['roles'])
