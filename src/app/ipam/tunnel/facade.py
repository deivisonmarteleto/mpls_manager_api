"""
Module responsible for facade of ipam tunnel
"""


from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import  DeleteRules

from src.app.core.ipam.devices.schema import DevicesSchema
from src.app.core.ipam.tunnel.models import TunnelBase
from src.app.core.ipam.tunnel.schema import TunnelSchema
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)


operation = "tunnel"


class TunnelFacade:
    """
    Class responsible for the facade of the tunnel
    """

    @staticmethod
    async def get_tunnel() -> CustomResponse:
        """
        Method responsible for get a tunnel by device id
        """

        logger.info("Facade: Get tunnel by device id...")
        try:

            find_tunnel = await TunnelSchema.find(
                fetch_links=True, nesting_depth=1
            ).to_list()

            logger.info("Facade: Get tunnel by device id success: %s", find_tunnel)
            return CustomResponse.success(message=FOUND.format(operation), data=find_tunnel)

        except Exception as err:
            logger.error("Error get tunnel by device id (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelFacade.get_tunnel_by_device]")

    @staticmethod
    async def create_tunnel(tunnel: Type[TunnelBase]) -> CustomResponse:
        """
        Method responsible for creating tunnel
        """

        logger.info("Facade: Creating tunnel...")
        try:
            create_tunnel = TunnelSchema(**tunnel.model_dump(exclude_unset=True))
            await create_tunnel.insert()

            logger.info("Facade: Creating tunnel success...")
            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, tunnel.name), data=create_tunnel)

        except DuplicateKeyError as err:
            logger.error("Error creating tunnel (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, tunnel.name))

        except Exception as err:
            logger.error("Error creating tunnel (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelFacade.create_tunnel]")

    @staticmethod
    async def delete_tunnel(tunnel_id: str) -> CustomResponse:
        """
        Method responsible for delete a tunnel
        """

        logger.info("Facade: Delete tunnel...")
        try:
            find_tunnel = await TunnelSchema.get(ObjectId(tunnel_id), fetch_links=True)
            if find_tunnel is None:
                logger.error("Tunnel %s not found!", tunnel_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, tunnel_id))

            await find_tunnel.delete()

            logger.info("Facade: Delete tunnel success...")
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, find_tunnel.name))

        except Exception as err:
            logger.error("Error delete tunnel (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelFacade.delete_tunnel]")

    @staticmethod
    async def update_tunnel(tunnel_id: str, tunnel: Type[TunnelBase]) -> CustomResponse:
        """
        Method responsible for update a tunnel
        """

        logger.info("Facade: Update tunnel...")
        try:
            find_tunnel = await TunnelSchema.find_one(TunnelSchema.id == ObjectId(tunnel_id), fetch_links=True)
            if find_tunnel is None:
                logger.error("Tunnel %s not found! [update]", tunnel_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, tunnel_id))

            logger.info("Facade: find tunnel success [update]: %s", find_tunnel.dict())
            for field, value in tunnel.model_dump(exclude_unset=True).items():
                if field in  ["id", "_id"]:
                    continue
                current_value = getattr(find_tunnel, field)

                if value != current_value or (value is None and current_value is not None):
                    logger.info("Facade: Update tunnel field: %s", field)
                    setattr(find_tunnel, field, value)

            update_tunnel = await find_tunnel.save()
            logger.info("Facade: Update tunnel success...")
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, tunnel.name), data=update_tunnel)

        except DuplicateKeyError as err:
            logger.error("Error update tunnel (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, tunnel.name))

        except Exception as err:
            logger.error("Error update tunnel (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelFacade.update_tunnel]")
