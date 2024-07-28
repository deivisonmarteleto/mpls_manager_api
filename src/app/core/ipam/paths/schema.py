
"""
Module responsible for paths schema
"""


from datetime import datetime
from typing import Annotated, Optional, Literal, List

from beanie import Document, Indexed, Link, BackLink
from pydantic import BaseModel, Field



class PathsSchema(Document):
    """
    Schema Document for paths
    """
    name:  Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    step_1: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_2: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_3: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_4: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_5: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_6: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_7: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_8: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_9: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_10: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_11: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_12: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_13: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_14: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_15: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_16: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_17: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_18: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_19: Optional[Link["DevicesSchema"]] = Field(default=None)
    step_20: Optional[Link["DevicesSchema"]] = Field(default=None)

    alarm: Optional[bool] = Field(default=False)
    info: Optional[dict] = Field(default={})
    options: Optional[dict] = Field(default={})

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)



    class Settings:
        name = "paths"
