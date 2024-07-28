"""
Module schema for ipam tunnel
"""
from datetime import datetime
from typing import Annotated, Literal, Optional, List

from beanie import Document, Indexed, BackLink, Link
from pydantic import Field
from src.app.core.ipam.paths.schema import PathsSchema


class TunnelSchema(Document):
    """
    Base for tunnel
    """
    name: Annotated[Optional[str], Indexed(unique=True)]
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tunnel_id: Annotated[Optional[int], Indexed(unique=True)]
    tunnel_type: Optional[Literal["static", "dynamic"]] = Field(default="static")
    status: Optional[bool] = Field(default=False)

    ### src
    path_primary_src : Optional[Link[PathsSchema]] = Field(default=None)
    path_secondary_src : Optional[Link[PathsSchema]] = Field(default=None)

    ### dst
    path_primary_dst : Optional[Link[PathsSchema]] = Field(default=None)
    path_secondary_dst : Optional[Link[PathsSchema]] = Field(default=None)


    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Settings:
        name = "tunnels"
