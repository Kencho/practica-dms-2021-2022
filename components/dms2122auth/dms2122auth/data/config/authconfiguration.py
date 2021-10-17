""" AuthConfiguration class module.
"""

from typing import Dict
from dms2122common.data.config import ServiceConfiguration


class AuthConfiguration(ServiceConfiguration):
    """ Class responsible of storing a specific authentication service configuration.
    """

    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.

        Returns:
            - str: A string identifying the component which will categorize the configuration.
        """

        return 'dms2122auth'

    def __init__(self):
        """ Initialization/constructor method.
        """

        ServiceConfiguration.__init__(self)

        self.set_db_connection_string('sqlite:////tmp/dms2122auth.sqlite3.db')
        self.set_service_host('127.0.0.1')
        self.set_service_port(4000)
        self.set_debug_flag(True)
        self.set_password_salt('This salt should be changed ASAP')
        self.set_jws_secret('This JWS secret should be changed ASAP')
        self.set_jws_ttl(3600)
        self.set_authorized_api_keys([])

    def _set_values(self, values: Dict) -> None:
        """Sets/merges a collection of configuration values.

        Args:
            - values (Dict): A dictionary of configuration values.
        """
        ServiceConfiguration._set_values(self, values)

        if 'db_connection_string' in values:
            self.set_db_connection_string(values['db_connection_string'])
        if 'salt' in values:
            self.set_password_salt(values['salt'])
        if 'jws_secret' in values:
            self.set_jws_secret(values['jws_secret'])
        if 'jws_ttl' in values:
            self.set_jws_ttl(values['jws_ttl'])

    def set_db_connection_string(self, db_connection_string: str) -> None:
        """ Sets the db_connection_string configuration value.

        Args:
            - db_connection_string: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['db_connection_string'] = str(db_connection_string)

    def get_db_connection_string(self) -> str:
        """ Gets the db_connection_string configuration value.

        Returns:
            - str: A string with the value of db_connection_string.
        """

        return str(self._values['db_connection_string'])

    def set_password_salt(self, salt: str) -> None:
        """ Sets the password salt configuration value.

        Args:
            - salt: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['salt'] = str(salt)

    def get_password_salt(self) -> str:
        """ Gets the password salt configuration value.

        Returns:
            - str: A string with the value of salt.
        """

        return str(self._values['salt'])

    def set_jws_secret(self, secret: str) -> None:
        """ Sets the JWS secret key configuration value.

        Args:
            - secret: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['jws_secret'] = str(secret)

    def get_jws_secret(self) -> str:
        """ Gets the JWS secret key configuration value.

        Returns:
            - str: A string with the value of jws_secret.
        """

        return str(self._values['jws_secret'])

    def set_jws_ttl(self, ttl: int) -> None:
        """ Sets the jws_ttl configuration value.

        Args:
            - ttl: An integer with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['jws_ttl'] = int(ttl)

    def get_jws_ttl(self) -> int:
        """ Gets the jws_ttl configuration value.

        Returns:
            - int: An integer with the value of jws_ttl.
        """

        return int(self._values['jws_ttl'])
