""" User class module.
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2122auth.data.db.results.resultbase import ResultBase
from dms2122auth.data.db.results.userrole import UserRole


class User(ResultBase):
    """ Definition and storage of user ORM records.
    """

    def __init__(self, username: str, password: str):
        """ Constructor method.

        Initializes a user record.

        Args:
            - username (str): A string with the user name.
            - password (str): A string with the password hash.
        """
        self.username: str = username
        self.password: str = password

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
            'users',
            metadata,
            Column('username', String(32), primary_key=True),
            Column('password', String(64), nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.

        Returns:
            - Dict: A dictionary with the mapping properties.
        """
        return {
            'rights': relationship(UserRole, backref='user')
        }
