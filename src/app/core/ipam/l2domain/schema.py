"""
Module responsible for l2 domain Schema
"""

from typing import Annotated, Optional

from beanie import Document, Indexed, Link

from src.app.core.facilities.locations.schema import LocationsSchema


class L2DomainSchema(Document):
    """
    Schema Document for L2 Domains
    """
    name: Annotated[str, Indexed(unique=True)]
    description: Optional[str]
    location : Optional[Link[LocationsSchema]]

    class Settings:
        name = "l2domains"
