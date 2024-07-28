"""
Module responsible for interface single models Base
"""

from typing import Optional, Literal
from pydantic import Field, BaseModel


class VendorBase(BaseModel):
    """
    Base for interface single
    """
    name: Optional[str]
    description: Optional[str] = Field(default=None)

