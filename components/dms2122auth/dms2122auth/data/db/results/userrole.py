""" UserRole class module.
"""

from sqlalchemy import Table, MetaData, Column, ForeignKey, String, Enum  # type: ignore
from dms2122common.data import Role
from dms2122auth.data.db.results.resultbase import ResultBase


class UserRole(ResultBase):
    """ Definition and storage of user role ORM records.
    """

    def __init__(self, username: str, role: Role):
        """ Constructor method.

        Initializes a user role record.

        Args:
            - username (str): A string with the user name.
            - role (Role): A string with the role.
        """
        self.username: str = username
        self.role: Role = role

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.

        Args:
            - metadata (MetaData): The database schema metadata
                        (used to gather the entities' definitions and mapping)

        Returns:
            - Table: A `Table` object with the table definition.
        """
        return Table(
            'user_roles',
            metadata,
            Column('username', String(32),
                   ForeignKey('users.username'), primary_key=True),
            Column('role', Enum(Role), primary_key=True)
        )
