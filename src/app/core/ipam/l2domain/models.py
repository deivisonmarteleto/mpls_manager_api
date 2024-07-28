"""
Module responsible for l2 domain models Base
"""

from typing import Optional
from pydantic import Field, BaseModel

class L2DomainBase(BaseModel):
    """
    Base for l2 domain
    """
    name: Optional[str]
    description: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
