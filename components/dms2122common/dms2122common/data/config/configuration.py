""" Module containing the dms2122common.data.config.configuration.Configuration class.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict
from appdirs import user_config_dir  # type: ignore
import yaml


class Configuration(ABC):
    """ Class responsible of storing a specific service configuration.
    """

    @abstractmethod
    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.

        Returns:
            - str: A string identifying the component which will categorize the configuration.
        """

        return ''

    def default_config_file(self) -> str:
        """ Path of the default configuration file.

        Returns:
            - str: A string with the path of the default configuration file.
        """

        return os.path.join(user_config_dir(self._component_name()), 'config.yml')

    def __init__(self):
        """ Initialization/constructor method.
        """

        self._values: Dict = {}

    def load_from_file(self, path: str = 'config.yml') -> None:
        """ Loads the configuration values from a given file.

        This operation will override any previously existing configuration parameters.

        Args:
            - path (str): A string with the path of the configuration file to load.
        """

        if os.path.isfile(path):
            with open(path, 'r') as stream:
                self._set_values(yaml.load(stream, Loader=yaml.SafeLoader))

    @abstractmethod
    def _set_values(self, values: Dict) -> None:
        """ Overrides the configuration values with a given dictionary.

        Args:
            - values (Dict): The dictionary of configuration values.
        """
