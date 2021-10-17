""" ServiceConfiguration class module.
"""

from typing import List, Dict
from .configuration import Configuration


class ServiceConfiguration(Configuration):
    """ Class responsible of storing an HTTP service configuration.
    """

    def __init__(self):
        """ Initialization/constructor method.
        """

        Configuration.__init__(self)

        self.set_authorized_api_keys([])

    def _set_values(self, values: Dict) -> None:
        """Sets/merges a collection of configuration values.

        Args:
            - values (Dict): A dictionary of configuration values.
        """
        if 'service_host' in values:
            self.set_service_host(values['service_host'])
        if 'service_port' in values:
            self.set_service_port(values['service_port'])
        if 'debug' in values:
            self.set_debug_flag(values['debug'])
        if 'authorized_api_keys' in values:
            self.set_authorized_api_keys(values['authorized_api_keys'])

    def set_service_host(self, service_host: str) -> None:
        """ Sets the service_host configuration value.

        Args:
            - service_host: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['service_host'] = str(service_host)

    def get_service_host(self) -> str:
        """ Gets the service_host configuration value.

        Returns:
            - str: A string with the value of service_host.
        """

        return str(self._values['service_host'])

    def set_service_port(self, service_port: int) -> None:
        """ Sets the service_port configuration value.

        Args:
            - service_port: An integer with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['service_port'] = int(service_port)

    def get_service_port(self) -> int:
        """ Gets the service_port configuration value.

        Returns:
            - int: An integer with the value of service_port.
        """

        return int(self._values['service_port'])

    def set_debug_flag(self, debug: bool) -> None:
        """ Sets whether the debug flag is set or not.

        Args:
            - debug: A boolean with the value of debug.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['debug'] = bool(debug)

    def get_debug_flag(self) -> bool:
        """ Gets whether the debug flag is set or not.

        Returns:
            - bool: A boolean with the value of debug.
        """

        return bool(self._values['debug'])

    def set_authorized_api_keys(self, keys: List[str]) -> None:
        """ Sets the authorized_api_keys configuration value.

        Args:
            - keys: A list of authorized API keys.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['authorized_api_keys'] = keys

    def get_authorized_api_keys(self) -> List[str]:
        """ Gets the authorized_api_keys configuration value.

        Returns:
            - List[str]: A list of strings with the value of authorized_api_keys.
        """

        return self._values['authorized_api_keys']
