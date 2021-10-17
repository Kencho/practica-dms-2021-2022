""" AdminEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, flash
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest import AuthService
from .webauth import WebAuth
from .webuser import WebUser


class AdminEndpoints():
    """ Monostate class responsible of handling the administrative web endpoint requests.
    """
    @staticmethod
    def get_admin(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the administration root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Admin.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('admin.html', name=name, roles=session['roles'])

    @staticmethod
    def get_admin_users(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the users administration endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Admin.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('admin/users.html', name=name, roles=session['roles'],
                               users=WebUser.list_users(auth_service)
                               )

    @staticmethod
    def get_admin_users_new(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the user creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Admin.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        redirect_to = request.args.get('redirect_to', default='/admin/users')
        return render_template('admin/users/new.html', name=name, roles=session['roles'],
                               redirect_to=redirect_to
                               )

    @staticmethod
    def post_admin_users_new(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the user creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Admin.name not in session['roles']:
            return redirect(url_for('get_home'))
        if request.form['password'] != request.form['confirmpassword']:
            flash('Password confirmation mismatch', 'error')
            return redirect(url_for('get_admin_users_new'))
        created_user = WebUser.create_user(auth_service,
                                           request.form['username'], request.form['password']
                                           )
        if not created_user:
            return redirect(url_for('get_admin_users_new'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_admin_users')
        return redirect(redirect_to)

    @staticmethod
    def get_admin_users_edit(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the user editing endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Admin.name not in session['roles']:
            return redirect(url_for('get_home'))
        name: str = session['user']
        username: str = str(request.args.get('username'))
        redirect_to: str = str(request.args.get(
            'redirect_to', default='/admin/users'))
        return render_template('admin/users/edit.html', name=name, roles=session['roles'],
                               username=username,
                               current_roles=WebUser.get_roles(auth_service, username),
                               all_roles=[name for name, member in Role.__members__.items()],
                               redirect_to=redirect_to
                               )

    @staticmethod
    def post_admin_users_edit(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the user editing endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Admin.name not in session['roles']:
            return redirect(url_for('get_home'))
        successful: bool = True
        successful &= WebUser.update_user_roles(auth_service,
                                                request.form['username'],
                                                request.form.getlist('roles')
                                                )
        session['roles'] = WebUser.get_roles(auth_service, session['user'])
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_admin_users')
        return redirect(redirect_to)
