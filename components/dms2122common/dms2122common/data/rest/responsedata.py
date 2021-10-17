""" ResponseData class module.
"""

from typing import List


class ResponseData():
    """ Entity class holding several data from REST requests.
    """
    def __init__(self):
        """ Constructor method.

        Creates a successful, no-content, no-messages instance.
        """
        self.set_successful(True)
        self.set_content(None)
        self.__messages: List[str] = []

    def set_successful(self, successful: bool):
        """ Sets the response successful flag.

        Args:
            - successful (bool): Whether the request was successful (`True`) or not.
        """
        self.__successful: bool = successful

    def is_successful(self) -> bool:
        """ Gets whether the request was successful (`True`) or not.

        Returns:
            - bool: `True` if the request was successful. `False` otherwise.
        """
        return self.__successful

    def set_content(self, content):
        """ Sets the content of the response.

        Args:
            - content (any): The content of the response.
        """
        self.__content = content

    def get_content(self):
        """ Gets the content of the response.

        Returns:
            - any: The content of the response.
        """
        return self.__content

    def add_message(self, message: str):
        """ Appends a message to the list of messages after processing a response.

        Args:
            - message (str): The message to append.
        """
        self.__messages.append(message)

    def add_messages(self, messages: List[str]):
        """ Appends several messages at a time.

        Args:
            - messages (List[str]): A list of messages to append.
        """
        for message in messages:
            self.__messages.append(message)

    def get_messages(self) -> List[str]:
        """ Gets the list of messages gathered after processing a response.

        Returns:
            - List[str]: The list of messages.
        """
        return self.__messages
