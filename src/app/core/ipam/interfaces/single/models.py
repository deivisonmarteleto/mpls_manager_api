"""
Module responsible for interface single models Base
"""

from typing import Optional, Literal
from pydantic import Field, BaseModel


class InterfaceSingleBase(BaseModel):
    """
    Base for interface single
    """
    name: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[bool] = Field(default=False)
    status_op: Optional[bool] = Field(default=False)
    mode: Optional[Literal["hybrid", "tag", "untag", "unknown"]] = Field(default="unknown")
    type: Optional[Literal["lag", "single"]] = Field(default="single")
    speed: Optional[Literal[10, 40, 100]] = Field(default=10)
    mtu: Optional[int] = Field(default=1500)
    operation_type: Optional[Literal["p2p-ce", "p2p-p", "p2p-pe"]] = Field(default="p2p-ce")

    vrf: Optional[str] = Field(default=None)
    vlans: Optional[list[str]] = Field(default=[])

    ipaddr : Optional[str] = Field(default=None)

    device: Optional[str] = Field(default=None)
    lag: Optional[str] = Field(default=None)

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
