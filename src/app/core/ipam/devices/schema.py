"""
Module responsible for devices Schema
"""

from datetime import datetime
from typing import Annotated, Optional, Literal, List

from beanie import Document, Indexed, Link, BackLink
from pydantic import BaseModel, Field

from src.app.core.ipam.devices.models import ( DevicesAccessBase,
                                                DevicesMonitoringBase,
                                                DevicesOsBase
                                                )
from src.app.core.ipam.interfaces.single.schema import InterfaceSingleSchema
from src.app.core.facilities.locations.schema import LocationsSchema
from src.app.core.facilities.vendors.schema import VendorSchema
from src.app.core.ipam.paths.schema import PathsSchema


class DevicesSchema(Document):
    """
    Schema Document for Devices
    """
    name: Annotated[Optional[str], Indexed(unique=True)] = Field(default=None)
    description: Optional[str] = Field(default=None)
    ipaddr: Optional[str] = Field(default=None)
    group: Optional[Literal["mpls", "metro ethernet", "fabric"]] = Field(default="mpls")
    model: Optional[str] = Field(default=None)
    status: Optional[Literal["enable", "disable"]] = Field(default="disable")
    monitoring: Optional[DevicesMonitoringBase] = Field(default_factory=DevicesMonitoringBase)
    access: Optional[DevicesAccessBase] = Field(default_factory=DevicesAccessBase)
    os: Optional[DevicesOsBase] = Field(default_factory=DevicesOsBase)

    vendor: Optional[Link[VendorSchema]] = Field(default=None)
    location : Optional[Link[LocationsSchema]] = Field(default=None)

    physical_interface: Optional[List[BackLink[InterfaceSingleSchema]]] = Field(default_factory=list, original_field="device")
    path: Optional[List[BackLink[PathsSchema]]]= Field(default_factory=list, original_field="step_1")

    info: Optional[dict] = Field(default={})
    alarm: Optional[bool] = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)

    class Settings:
        name = "devices"
