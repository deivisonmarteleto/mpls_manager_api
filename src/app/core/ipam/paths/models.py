"""
Module responsible for paths models Base
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import Field, BaseModel






class PathsBase(BaseModel):
    """
    Base for circuits
    """
    name:  Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    step_1: Optional[str] = Field(default=None)
    step_2: Optional[str] = Field(default=None)
    step_3: Optional[str] = Field(default=None)
    step_4: Optional[str] = Field(default=None)
    step_5: Optional[str] = Field(default=None)
    step_6: Optional[str] = Field(default=None)
    step_7: Optional[str] = Field(default=None)
    step_8: Optional[str] = Field(default=None)
    step_9: Optional[str] = Field(default=None)
    step_10: Optional[str] = Field(default=None)
    step_11: Optional[str] = Field(default=None)
    step_12: Optional[str] = Field(default=None)
    step_13: Optional[str] = Field(default=None)
    step_14: Optional[str] = Field(default=None)
    step_15: Optional[str] = Field(default=None)
    step_16: Optional[str] = Field(default=None)
    step_17: Optional[str] = Field(default=None)
    step_18: Optional[str] = Field(default=None)
    step_19: Optional[str] = Field(default=None)
    step_20: Optional[str] = Field(default=None)

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
