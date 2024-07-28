"""
Module responsible for tunnel models Base
"""


from datetime import datetime
from typing import Literal, Optional
from pydantic import Field, BaseModel


class TunnelBase(BaseModel):
    """
    Base for tunnel
    """
    name: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tunnel_id: Optional[int] = Field(default=None)
    tunnel_type: Optional[Literal["static", "dynamic"]] = Field(default="static")
    status: Optional[bool] = Field(default=False)

    ### src
    path_primary_src : Optional[str] = Field(default=None)
    path_secondary_src : Optional[str] = Field(default=None)

    ### dst
    path_primary_dst : Optional[str] = Field(default=None)
    path_secondary_dst : Optional[str] = Field(default=None)


    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
