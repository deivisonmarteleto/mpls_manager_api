"""
Module responsible for locations Schema
"""

from typing import Annotated, Optional
from pydantic import Field

from beanie import Document, Indexed

from src.app.core.facilities.locations.models import LocationsAccessBase

class LocationsSchema(Document):
    """
    Schema Document for locations
    """
    name: Annotated[str, Indexed(unique=True)]
    description: Optional[str] = Field(default=None)
    postal_code: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    number: Optional[int] = Field(default=None)
    complement: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default="Brasil")
    lat: Optional[str] = Field(default=None)
    lng: Optional[str] = Field(default=None)
    access: LocationsAccessBase = Field(default_factory=LocationsAccessBase)

    class Settings:
        name = "locations"