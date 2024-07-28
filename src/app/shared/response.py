"""
Responsibility module for custom response
"""
from typing import Any

class CustomResponse:
    """
    Class Custom Response
    """

    @staticmethod
    def success(message: str = None, data: Any = None) -> dict[str:str]:
        """
        role responsible for the success message
        """
        response: dict = {}
        response["status"] = "success"
        response["message"] = message
        response["data"] = data

        return response

    @staticmethod
    def failure(message: str = None, data: Any = None) -> dict[str:str]:
        """
        function responsible for the fault message
        """
        response: dict = {}
        response["status"] = "failure"
        response["message"] = message
        response["data"] = data

        return response
