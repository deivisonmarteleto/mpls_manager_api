"""
Module responsible for vrf Schema
"""

from typing import Annotated, Optional
from pydantic import Field

from beanie import Document, Indexed
from src.app.core.ipam.vrf.models import BgpBase, OspfBase, StaticRouteBase


class VrfSchema(Document):
    """
    Schema Document for vrf
    """
    name: Annotated[Optional[str], Indexed(unique=True)]
    description: Optional[str]


    rd: Optional[str] = Field(default=None)
    rt_import: Optional[str] = Field(default=None)
    rt_export: Optional[str] = Field(default=None)

    bgp: Optional[list[BgpBase]] = Field(default=[])
    ospf: Optional[list[OspfBase]] = Field(default=[])
    static_route: Optional[list[StaticRouteBase]] = Field(default=[])

    class Settings:
        name = "vrfs"
