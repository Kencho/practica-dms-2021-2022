""" RoleServices class module.
"""

from typing import Union, List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122common.data import Role
from dms2122auth.data.db import Schema
from dms2122auth.data.db.exc.usernotfounderror import UserNotFoundError
from dms2122auth.data.db.results import UserRole
from dms2122auth.data.db.resultsets import UserRoles


class RoleServices():
    """ Monostate class that provides high-level services to handle role-related use cases.
    """
    @staticmethod
    def has_role(username: str, role: Union[Role, str], schema: Schema) -> bool:
        """Determines whether a user has a certain role or not.

        Args:
            - username (str): The username of the user to test.
            - role (Union[Role, str]): The role to be tested.
            - schema (Schema): A database handler where users and roles are mapped into.

        Returns:
            - bool: `True` if the user has the given role. `False` otherwise.
        """
        session: Session = schema.new_session()
        has_role: bool
        try:
            if isinstance(role, str):
                role = Role[role]
            has_role = bool(UserRoles.find_role(
                session, username, role) is not None)
        except KeyError:
            has_role = False
        except UserNotFoundError:
            has_role = False
        schema.remove_session()
        return has_role

    @staticmethod
    def list_user_roles(username: str, schema: Schema) -> List[str]:
        """Lists the roles assigned to a given user.

        Args:
            - username (str): The username of the user queried.
            - schema (Schema): A database handler where users and roles are mapped into.

        Raises:
            - ValueError: If the username is missing.

        Returns:
            - List[str]: The list of role names.
        """
        session: Session = schema.new_session()
        out: List[str] = []
        try:
            roles: List[UserRole] = UserRoles.list_all_for_user(
                session, username)
            for role in roles:
                out.append(role.role.name)
        except:  # pylint: disable=try-except-raise
            raise
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def grant_role(username: str, role: Union[Role, str], schema: Schema) -> None:
        """Grants a role to a user.

        Args:
            - username (str): The user name.
            - role (Union[Role, str]): The role to be granted.
            - schema (Schema): A database handler where users and roles are mapped into.

        Raises:
            - ValueError: If either the username or the role name is missing.
            - UserNotFoundError: If the user granted the role does not exist.
        """
        session: Session = schema.new_session()
        try:
            if isinstance(role, str):
                role = Role[role]
            UserRoles.grant(session, username, role)
        except:  # pylint: disable=try-except-raise
            raise
        finally:
            schema.remove_session()

    @staticmethod
    def revoke_role(username: str, role: Union[Role, str], schema: Schema) -> None:
        """Revokes a role from a user.

        Args:
            - username (str): The user name.
            - role (Union[Role, str]): The role to be granted.
            - schema (Schema): A database handler where users and roles are mapped into.

        Raises:
            - ValueError: If either the username or the role name is missing.
        """
        session: Session = schema.new_session()
        try:
            if isinstance(role, str):
                role = Role[role]
            UserRoles.revoke(session, username, role)
        except:  # pylint: disable=try-except-raise
            raise
        finally:
            schema.remove_session()
