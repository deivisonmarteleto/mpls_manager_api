"""
Module responsible for locations models Base
"""

from typing import Literal, Optional
from pydantic import Field, BaseModel


class LocationsAccessBase(BaseModel):
    """
    Base for access
    """

    contact: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    intranet: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class LocationsBase(BaseModel):
    """
    Base for coletions
    """

    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    postal_code: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    number: Optional[int] = Field(default=None)
    complement: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    lat: Optional[str] = Field(default=None)
    lng: Optional[str] = Field(default=None)
    access: LocationsAccessBase = Field(default_factory=LocationsAccessBase)
