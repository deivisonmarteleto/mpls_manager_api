"""
Module responsible for tunnel traffic policies models Base
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import Field, BaseModel






class TunnelTrafficPoliciesBase(BaseModel):
    """
    Base for tunnel traffic policies
    """
    name:  Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    step_1: Optional[str] = Field(default=None)
    step_2: Optional[str] = Field(default=None)
    step_3: Optional[str] = Field(default=None)
    step_4: Optional[str] = Field(default=None)
    step_5: Optional[str] = Field(default=None)


    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
