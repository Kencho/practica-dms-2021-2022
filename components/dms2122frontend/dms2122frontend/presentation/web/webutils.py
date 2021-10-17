""" WebUtils class module.
"""

from flask import flash
from dms2122common.data.rest import ResponseData


class WebUtils():
    """ Monostate class responsible of various operation utilities.
    """
    @staticmethod
    def flash_response_messages(response: ResponseData):
        """ "Flashes" the messages stored in a response if it was not successful.

        Args:
            - response (ResponseData): The response data object.
        """
        if not response.is_successful():
            for message in response.get_messages():
                flash(message, 'error')
