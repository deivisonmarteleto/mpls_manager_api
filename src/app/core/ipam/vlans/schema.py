"""
Module responsible for vlan Schema
"""

from typing import Annotated, Optional

from beanie import Document, Indexed, Link
from pydantic import Field

from src.app.core.ipam.l2domain.schema import L2DomainSchema


class VlanSchema(Document):
    """
    Schema Document for vlan
    """
    name: Annotated[str, Indexed()]
    alias: Optional[str]
    description: Optional[str]
    number: Annotated[int, Indexed()]
    l2domain : Optional[Link[L2DomainSchema]]
    unique: Optional[bool] = Field(default=False)

    class Settings:
        name = "vlans"
