"""
Module responsible for interface Lag models Base
"""

from typing import Optional, Literal
from pydantic import Field, BaseModel


class InterfaceLagBase(BaseModel):
    """
    Base for interface lag
    """
    name: Optional[str]
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[bool] = Field(default=False)
    mode: Optional[Literal["hybrid", "tag", "untag"]] = Field(default="untag")
    speed: Optional[Literal[10,20,40,80, 100, 200,300,400, 800]] = Field(default=20)
    mtu: Optional[int] = Field(default=1500)
    operation_type: Optional[Literal["p2p-ce", "p2p-p", "p2p-pe"]] = Field(default="p2p-pe")

    vrf: Optional[str] = Field(default=None)
    vlan: Optional[list[str]] = Field(default=[])
    ipaddr : Optional[str] = Field(default=None)
    interface: Optional[list[str]] = Field(default=[])

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
