"""
Module responsible for vlan models Base
"""

from typing import Optional
from pydantic import Field, BaseModel, validator

class VlanBase(BaseModel):
    """
    Base for vlan
    """
    name: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    number: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)
    l2domain: Optional[str] = Field(default=None)
    unique: Optional[bool] = Field(default=False)

    @validator('number')
    def check_ranger(cls, v):
        """
        Check if vlan number is in range
        """
        if v < 1 or v > 4095:
            raise ValueError('Range permitido: 2 a 4094')
        return v
