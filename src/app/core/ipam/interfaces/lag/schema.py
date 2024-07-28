"""
Module responsible for interface lag Schema
"""

from typing import Annotated, Optional,Literal, List
from pydantic import Field

from beanie import Document, Indexed, BackLink
from src.app.core.ipam.interfaces.single.schema import InterfaceSingleSchema
from src.app.core.ipam.vrf.schema import VrfSchema
from src.app.core.ipam.vlans.schema import VlanSchema


class InterfaceLagSchema(Document):
    """
    Schema Document for interface lag
    """
    name: Annotated[Optional[str], Indexed()]
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[bool] = Field(default=False)
    mode: Optional[Literal["hybrid", "tag", "untag"]] = Field(default="untag")
    speed: Optional[Literal[10,20,40,80, 100, 200,300,400, 800]] = Field(default=20)
    mtu: Optional[int] = Field(default=1500)
    ipaddr : Optional[str] = Field(default=None)
    operation_type: Optional[Literal["p2p-ce", "p2p-p", "p2p-pe"]] = Field(default="p2p-pe")

    vrf: Optional[VrfSchema] = Field(default=None)
    vlan: Optional[list[VlanSchema]] = Field(default=[])
    interface: Optional[List[BackLink[InterfaceSingleSchema]]] = Field(default_factory=list, original_field="lag")

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})

    class Settings:
        name = "interfaces_lag"
