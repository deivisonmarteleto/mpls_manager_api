
"""
Module responsible for circuits schema
"""


from datetime import datetime
from typing import Annotated, Optional, Literal

from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from src.app.core.ipam.interfaces.lag.schema import InterfaceLagSchema
from src.app.core.ipam.interfaces.single.schema import InterfaceSingleSchema
from src.app.core.ipam.tunnel_traffic_policies.schema import TunnelTrafficPoliciesSchema
from src.app.core.ipam.vlans.schema import VlanSchema



class CircuitsSchema(Document):
    """
    Schema Document for Circuits
    """
    name: Annotated[Optional[str], Indexed(unique=True)]
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    designation: Optional[str] = Field(default=None)
    project: Optional[str] = Field(default=None)
    owner_group: Optional[str] = Field(default=None)

    interface_src: Optional[Link[InterfaceSingleSchema]] = Field(default=None)
    interface_dst: Optional[Link[InterfaceSingleSchema]] = Field(default=None)

    lag_src: Optional[Link[InterfaceLagSchema]] = Field(default=None)
    lag_dst: Optional[Link[InterfaceLagSchema]] = Field(default=None)

    bind_policy: Optional[Link[TunnelTrafficPoliciesSchema]] = Field(default=None)

    vc_id: Annotated[Optional[int], Indexed(unique=True)]
    vc_type: Optional[str] = Field(default=None)
    vlan_tag: Optional[str] = Field(default=None)

    bandwidth_reservation: Optional[int] = Field(default=0)

    status: Optional[bool] = Field(default=False)

    criticality_matrix:  Optional[Literal[0,1,2,3,4,5]] = Field(default=0)
    type: Optional[Literal["vpn-l2", "vpn-l3", "pw", "vsi", "other"]] = Field(default="other")
    mtu: Optional[int] = Field(default=1500)

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Settings:
        name = "circuits"
