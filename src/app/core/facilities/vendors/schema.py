"""
Module responsible for vendor Schema
"""

from typing import Annotated, Optional

from beanie import Document, Indexed


class VendorSchema(Document):
    """
    Schema Document for Vendors
    """
    name: Annotated[str, Indexed(unique=True)]
    description: Optional[str]

    class Settings:
        name = "vendors"
