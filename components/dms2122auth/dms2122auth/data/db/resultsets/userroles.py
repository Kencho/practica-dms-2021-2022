""" UserRoles class module.
"""

from typing import Optional, List
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122common.data import Role
from dms2122auth.data.db.results import UserRole
from dms2122auth.data.db.exc import UserNotFoundError


class UserRoles():
    """ Class responsible of table-level user rights operations.
    """
    @staticmethod
    def grant(session: Session, username: str, role: Role) -> UserRole:
        """ Grants a role to a user.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - username (str): The user name string.
            - role (Role): The role name.

        Raises:
            - ValueError: If either the username or the role name is missing.
            - UserNotFoundError: If the user granted the role does not exist.

        Returns:
            - UserRole: The created `UserRole` result.
        """
        if not username or not role:
            raise ValueError('A username and a role name are required.')
        user_role: Optional[UserRole] = UserRoles.find_role(session, username, role)
        if user_role is not None:
            return user_role
        try:
            new_user_role = UserRole(username, role)
            session.add(new_user_role)
            session.commit()
            return new_user_role
        except IntegrityError as ex:
            session.rollback()
            raise UserNotFoundError() from ex
        except:
            session.rollback()
            raise

    @staticmethod
    def revoke(session: Session, username: str, role: Role):
        """ Revokes a role from a user.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - username (str): The user name string.
            - role (Role): The role name.

        Raises:
            - ValueError: If either the username or the role name is missing.
        """
        if not username or not role:
            raise ValueError('A username and a role name are required.')
        user_role: Optional[UserRole] = UserRoles.find_role(session, username, role)
        if user_role is None:
            return
        try:
            session.delete(user_role)
            session.commit()
        except:
            session.rollback()
            raise

    @staticmethod
    def find_role(session: Session, username: str, role: Role) -> Optional[UserRole]:
        """ Finds a role for a user.

        Args:
            - session (Session): The session object.
            - username (str): The user name string.
            - role (Role): The role name.

        Raises:
            - ValueError: If either the username or the role name is missing.

        Returns:
            - UserRole: The `UserRole` result if found, or `None` if the user does not have
              the given role.
        """
        if not username or not role:
            raise ValueError('A username and a role name are required.')
        try:
            query = session.query(UserRole).filter_by(
                username=username,
                role=role
            )
            return query.one()
        except NoResultFound:
            return None

    @staticmethod
    def list_all_for_user(session: Session, username: str) -> List[UserRole]:
        """Lists the `UserRole`s assigned to a certain user.

        Args:
            - session (Session): The session object.
            - username (str): The user name string.

        Raises:
            - ValueError: If the username is missing.

        Returns:
            - List[UserRole]: A list of `UserRole` registers with the user roles.
        """
        if not username:
            raise ValueError('A username is required.')
        query = session.query(UserRole).filter_by(
            username=username
        )
        return query.all()
