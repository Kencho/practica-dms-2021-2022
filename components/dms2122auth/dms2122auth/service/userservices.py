""" UserServices class module.
"""

from typing import List, Dict
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122auth.data.config import AuthConfiguration
from dms2122auth.data.db import Schema
from dms2122auth.data.db.results import User
from dms2122auth.data.db.resultsets import Users


class UserServices():
    """ Monostate class that provides high-level services to handle user-related use cases.
    """
    @staticmethod
    def user_exists(username: str, password: str, schema: Schema, cfg: AuthConfiguration) -> bool:
        """Determines whether a user with the given credentials exists.

        Args:
            - username (str): The user name.
            - password (str): The user password.
            - schema (Schema): A database handler where the users are mapped into.
            - cfg (AuthConfiguration): The application configuration.

        Returns:
            - bool: `True` if the given user exists. `False` otherwise.
        """
        salt: str = cfg.get_password_salt()
        password_hash: str = Users.hash_password(
            password, suffix=username, salt=salt)
        session: Session = schema.new_session()
        user_exists: bool = Users.user_exists(session, username, password_hash)
        schema.remove_session()
        return user_exists

    @staticmethod
    def list_users(schema: Schema) -> List[Dict]:
        """Lists the existing users.

        Args:
            - schema (Schema): A database handler where the users are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the users' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        users: List[User] = Users.list_all(session)
        for user in users:
            out.append({
                'username': user.username
            })
        schema.remove_session()
        return out

    @staticmethod
    def create_user(username: str, password: str, schema: Schema, cfg: AuthConfiguration) -> Dict:
        """Creates a user.

        Args:
            - username (str): The new user's name.
            - password (str): The new user's password.
            - schema (Schema): A database handler where the users are mapped into.
            - cfg (AuthConfiguration): The application configuration.

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new user's data.
        """
        salt: str = cfg.get_password_salt()
        password_hash: str = Users.hash_password(
            password, suffix=username, salt=salt)
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_user: User = Users.create(session, username, password_hash)
            out['username'] = new_user.username
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
