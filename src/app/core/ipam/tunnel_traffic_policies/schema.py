
"""
Module responsible for paths schema
"""


from datetime import datetime
from typing import Annotated, Optional, Literal

from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from src.app.core.ipam.tunnel.schema import TunnelSchema



class TunnelTrafficPoliciesSchema(Document):
    """
    Schema Document for paths
    """
    name:  Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    step_1: Optional[Link[TunnelSchema]] = Field(default=None)
    step_2: Optional[Link[TunnelSchema]] = Field(default=None)
    step_3: Optional[Link[TunnelSchema]] = Field(default=None)
    step_4: Optional[Link[TunnelSchema]] = Field(default=None)
    step_5: Optional[Link[TunnelSchema]] = Field(default=None)

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Settings:
        name = "tunnel_traffic_policies"
