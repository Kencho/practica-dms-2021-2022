""" FrontendConfiguration class module.
"""

from typing import Dict
from dms2122common.data.config import ServiceConfiguration


class FrontendConfiguration(ServiceConfiguration):
    """ Class responsible of storing a specific frontend configuration.
    """

    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.

        Returns:
            - str: A string identifying the component which will categorize the configuration.
        """

        return 'dms2122frontend'

    def __init__(self):
        """ Initialization/constructor method.
        """

        ServiceConfiguration.__init__(self)

        self.set_service_host('127.0.0.1')
        self.set_service_port(8080)
        self.set_debug_flag(True)
        self.set_app_secret_key('An ultra-secret key that will be used to sign the session cookie')
        self.set_auth_service({
            'host': '127.0.0.1',
            'port': 4000,
            'apikey_secret': 'This should be the frontend API key'
        })
        self.set_backend_service({
            'host': '127.0.0.1',
            'port': 5000,
            'apikey_secret': 'This is another frontend API key'
        })

    def _set_values(self, values: Dict) -> None:
        """Sets/merges a collection of configuration values.

        Args:
            - values (Dict): A dictionary of configuration values.
        """
        ServiceConfiguration._set_values(self, values)

        if 'app_secret_key' in values:
            self.set_app_secret_key(values['app_secret_key'])
        if 'auth_service' in values:
            self.set_auth_service(values['auth_service'])
        if 'backend_service' in values:
            self.set_backend_service(values['backend_service'])

    def set_app_secret_key(self, app_secret_key: str) -> None:
        """ Sets the app_secret_key configuration value.

        Args:
            - app_secret_key: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['app_secret_key'] = str(app_secret_key)

    def get_app_secret_key(self) -> str:
        """ Gets the app_secret_key configuration value.

        Returns:
            - str: A string with the value of app_secret_key.
        """

        return str(self._values['app_secret_key'])

    def set_auth_service(self, auth_service: Dict) -> None:
        """Sets the connection parameters for the authentication service.

        Args:
            auth_service (Dict): Parameters to connect to the authentication service.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['auth_service'] = auth_service

    def get_auth_service(self) -> Dict:
        """ Gets the authentication service configuration value.

        Returns:
            - Dict: A dictionary with the value of auth_service.
        """

        return self._values['auth_service']

    def set_backend_service(self, backend_service: Dict) -> None:
        """Sets the connection parameters for the backend service.

        Args:
            backend_service (Dict): Parameters to connect to the backend service.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['backend_service'] = backend_service

    def get_backend_service(self) -> Dict:
        """ Gets the backend service configuration value.

        Returns:
            - Dict: A dictionary with the value of backend_service.
        """

        return self._values['backend_service']
