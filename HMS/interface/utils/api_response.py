"""
This module provides a collection of utility functions that offer commonly used functionality
across the application or project.
"""

import inspect
from typing import Union

from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """This class will create a custom API response."""

    def __init__(self) -> None:
        self.caller_function = inspect.stack()[1].function

    def struct_response(
            self, data: dict, success: bool, message: str, errors=None
    ) -> dict:
        response = dict(success=success, message=message, data=data)
        if errors:
            response["errors"] = errors
        return response

    def success_message(self):
        return f'{self.caller_function.replace("_", "-").title()} Successful.'

    def success(self, status, data: dict = {}, message: str = None) -> Response:
        """This method will create a custom response for success event with response status 200."""
        try:
            success_message = message if message else self.success_message()
            response_data = self.struct_response(
                data=data, success=True, message=success_message
            )
            return Response(response_data, status=status)

        except Exception as e:
            raise Exception("Error:", e)

    def fail(self, status, errors: dict, message: Union[str, dict]) -> Response:
        """This method will create custom response for failure event with custom response status."""
        error_message = (
            message[next(iter(message))][0] if isinstance(message, dict) else message
        )
        response_data = self.struct_response(
            data={}, success=False, message=error_message, errors=errors
        )
        return Response(response_data, status=status)
