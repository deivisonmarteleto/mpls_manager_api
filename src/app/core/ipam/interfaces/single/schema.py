"""
Module responsible for vendor Schema
"""

from typing import Annotated, Literal, Optional, List

from beanie import Document, Indexed, BackLink, Link
from pydantic import Field

from src.app.core.ipam.vrf.schema import VrfSchema
from src.app.core.ipam.vlans.schema import VlanSchema


class InterfaceSingleSchema(Document):
    """
    Schema Document for Vendors
    """
    name: Annotated[Optional[str], Indexed()]
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[bool] = Field(default=False)
    status_op: Optional[bool] = Field(default=False)
    mode: Optional[Literal["hybrid", "tag", "untag", "unknown"]] = Field(default="untag")
    type: Optional[Literal["lag", "single"]] = Field(default="single")
    speed: Optional[Literal[10, 40, 100]] = Field(default=10)
    mtu: Optional[int] = Field(default=1500)
    operation_type: Optional[Literal["p2p-ce", "p2p-p", "p2p-pe"]] = Field(default="p2p-pe")

    ipaddr : Optional[str] = Field(default=None)

    vrf: Optional[VrfSchema] = Field(default=None)
    vlan: Optional[list[VlanSchema]] = Field(default=[])

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})

    lag: Optional[Link["InterfaceLagSchema"]] = Field(default=None)
    device: Optional[Link["DevicesSchema"]] = Field(default=None)

    class Settings:
        name = "interfaces_single"
