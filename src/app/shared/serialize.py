"""
Module for serialize response
"""

from typing import Any

from beanie import Link, BackLink
from fastapi.encoders import jsonable_encoder


class SerializationFilter:
    """
    Class responsible for filtering the response
    """

    @staticmethod
    def response(_object: Any) -> Any:
        """
        Method responsible for filtering the response
        """
        if isinstance(_object, list):
            for value in _object:
                SerializationFilter.response(value)
        elif hasattr(_object, "__dict__"):
            for key, value in _object.__dict__.items():
                if isinstance(value, Link):
                    _object.__dict__[key] = None

                elif isinstance(value, BackLink):
                    if isinstance(_object, list):
                        for item in _object:
                            SerializationFilter.response(item)
                    else:
                        _object.__dict__[key] = None

                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, BackLink):
                            _object.__dict__[key] = None
                        else:
                            SerializationFilter.response(item)
                else:
                    SerializationFilter.response(value)

        return jsonable_encoder(_object)
