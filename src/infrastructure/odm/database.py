"""
Module for the database ODM (Object Document Mapper) connection
"""
import motor.motor_asyncio
from beanie import init_beanie


async def init_db(db_host: str,  db_name):
    """
    Method responsible for initializing the database mongo
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{db_host}/{db_name}"
    )

    await init_beanie(
        database=client[db_name],
        document_models=[
            "src.app.core.facilities.vendors.schema.VendorSchema",
            "src.app.core.facilities.locations.schema.LocationsSchema",

            "src.app.core.ipam.devices.schema.DevicesSchema",
            "src.app.core.ipam.interfaces.single.schema.InterfaceSingleSchema",
            "src.app.core.ipam.interfaces.lag.schema.InterfaceLagSchema",
            "src.app.core.ipam.vrf.schema.VrfSchema",
            "src.app.core.ipam.circuits.schema.CircuitsSchema",
            "src.app.core.ipam.l2domain.schema.L2DomainSchema",
            "src.app.core.ipam.vlans.schema.VlanSchema",
            "src.app.core.ipam.tunnel.schema.TunnelSchema",
            "src.app.core.ipam.tunnel_traffic_policies.schema.TunnelTrafficPoliciesSchema",
            "src.app.core.ipam.paths.schema.PathsSchema",

        ]
    )
