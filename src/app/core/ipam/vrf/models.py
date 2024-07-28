"""
Module responsible for vrf models Base
"""

from typing import Optional, Literal
from pydantic import Field, BaseModel




class BgpBase(BaseModel):
    """
    Base for bgp
    """
    name: Optional[str]
    description: Optional[str] = Field(default=None)

    asn: Optional[int] = Field(default=None)
    router_id: Optional[str] = Field(default=None)
    neighbor: Optional[str] = Field(default=None)

class OspfBase(BaseModel):
    """
    Base for ospf
    """
    name: Optional[str]
    description: Optional[str] = Field(default=None)

    router_id: Optional[str] = Field(default=None)
    area: Optional[str] = Field(default=None)
    network: Optional[str] = Field(default=None)

class StaticRouteBase(BaseModel):
    """
    Base for static route
    """
    name: Optional[str]
    description: Optional[str] = Field(default=None)

    network: Optional[str] = Field(default=None)
    next_hop: Optional[str] = Field(default=None)



class VrfBase(BaseModel):
    """
    Base for vrf
    """
    name: Optional[str]
    description: Optional[str] = Field(default=None)

    rd: Optional[str] = Field(default=None)
    rt_import: Optional[str] = Field(default=None)
    rt_export: Optional[str] = Field(default=None)

    bgp: Optional[list[BgpBase]] = Field(default=[])
    ospf: Optional[list[OspfBase]] = Field(default=[])
    static_route: Optional[list[StaticRouteBase]] = Field(default=[])
