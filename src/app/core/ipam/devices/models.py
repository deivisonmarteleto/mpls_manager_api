"""
Module responsible for devices models Base
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import Field, BaseModel


class DevicesOsBase(BaseModel):
    """
    Base for devices os
    """
    type: Optional[Literal["linux", "windows", "cisco", "nokia", "huawei", "freeBSD", "outros"]] = Field(default="outros")
    version: Optional[str] = Field(default=None)
    options: Optional[dict] = Field(default={})


class DevicesAccessBase(BaseModel):
    """
    Base for devices access
    """
    status: Optional[bool] = Field(default=False)
    type: Optional[Literal["ssh", "telnet", "http", "https", "tl1", "sshkey"]] = Field(default="ssh")
    options: Optional[dict] = Field(default={})
    username: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    port: Optional[int] = Field(default=None)
    ssh_key: Optional[str] = Field(default=None)


class DevicesMonitoringBase(BaseModel):
    """
    Base for devices monitoring
    """
    status: Optional[bool] = Field(default=False)
    type: Optional[Literal["snmp", "icmp", "http"]] = Field(default="icmp")
    snmp_community: Optional[str] = Field(default="public")
    snmp_version: Optional[Literal["v1", "v2", "v3"]] = Field(default="v2c")
    snmp_port: Optional[int] = Field(default=161)
    options: Optional[dict] = Field(default={})
    group_id: Optional[str] = Field(default=None)
    template_id: Optional[str] = Field(default=None)
    zabbix_id: Optional[int] = Field(default=None)


class DevicesBase(BaseModel):
    """
    Base for devices
    """
    name: Optional[str] = Field(default=None)
    ipaddr: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    group: Optional[Literal["mpls", "metro ethernet", "fabric"]] = Field(default="mpls")
    model: Optional[str] = Field(default=None)
    vendor: Optional[str] = Field(default=None)
    status: Optional[Literal["enable", "disable"]] = Field(default="disable")
    monitoring: Optional[DevicesMonitoringBase] = Field(default_factory=DevicesMonitoringBase)
    access: Optional[DevicesAccessBase] = Field(default_factory=DevicesAccessBase)
    os: Optional[DevicesOsBase] = Field(default_factory=DevicesOsBase)
    location: Optional[str] = Field(default=None)

    physical_interface: Optional[list] = Field(default=[])
    path: Optional[list] = Field(default=[])


    info: Optional[dict] = Field(default={})
    alarm: Optional[bool] = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)
