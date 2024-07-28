"""
Module responsible for circuits models Base
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import Field, BaseModel






class CircuitsBase(BaseModel):
    """
    Base for circuits
    """
    name:  Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    designation: Optional[str] = Field(default=None)
    project: Optional[str] = Field(default=None)
    owner_group: Optional[str] = Field(default=None)

    interface_src: Optional[str] = Field(default=None)
    interface_dst:  Optional[str] = Field(default=None)

    lag_src:  Optional[str] = Field(default=None)
    lag_dst:  Optional[str] = Field(default=None)

    bind_policy: Optional[str] = Field(default=None)

    vc_id: Optional[int] = Field(default=None)
    vc_type: Optional[str] = Field(default=None)
    vlan_tag:  Optional[str] = Field(default=None)

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
