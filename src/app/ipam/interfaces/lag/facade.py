"""
Module for lag interfaces lag
"""

from datetime import datetime
from typing import Type

from beanie.operators import In
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.core.ipam.interfaces.lag.models import InterfaceLagBase
from src.app.core.ipam.interfaces.lag.schema import InterfaceLagSchema
from src.app.core.ipam.interfaces.single.schema import \
    InterfaceSingleSchema
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)


operation = "interface lag"


class InterfaceLagFacade:
    """
    Class responsible for the facade of the interface lag
    """

    @staticmethod
    async def create_interface_lag(interface: Type[InterfaceLagBase], interface_id=str) -> CustomResponse:
        """
        Method responsible for creating interface lag
        """

        logger.info("Facade: Creating interface lag...")
        try:
            find_interface = await InterfaceSingleSchema.get(ObjectId(interface_id), fetch_links=True)
            if find_interface is None:
                logger.error("Interface  %s not found!", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, interface_id))

            create_interface_lag = InterfaceLagSchema(**interface.model_dump(exclude_unset=True))
            await create_interface_lag.insert()

            find_interface.lag = create_interface_lag
            find_interface.ipaddr = None
            find_interface.type = "lag"
            find_interface.mode = "unknown"
            find_interface.vrf = None
            find_interface.vlan = None

            await find_interface.save()

            logger.info("Facade: Creating interface lag success: %s", create_interface_lag.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, interface.name), data=create_interface_lag)

        except DuplicateKeyError as err:
            logger.error("Error creating interface lag (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, interface.name))

        except Exception as err:
            logger.error("Error creating interface lag (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.create_interface_lag]")

    @staticmethod
    async def detach_interface_lag(interface_id: str) -> CustomResponse:
        """
        Method responsible for deattach a interface lag
        """

        logger.info("Facade: Deattach interface lag...")
        try:
            find_interface = await InterfaceSingleSchema.get(ObjectId(interface_id), fetch_links=True)
            if find_interface is None:
                logger.error("Interface  %s not found!", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format("Interface  ", interface_id))

            if find_interface.lag is None:
                logger.error("Interface  %s not have lag!", interface_id)
                return CustomResponse.failure(message="Interface not have lag")

            logger.info("Facade: find interface lag success: %s", find_interface.dict())
            find_interface.lag = None
            await find_interface.save()

            logger.info("Facade: Deattach interface lag success: %s", find_interface.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, find_interface.name), data=find_interface)

        except DuplicateKeyError as err:
            logger.error("Error deattach interface lag (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, find_interface.name))

        except Exception as err:
            logger.error("Error deattach interface lag (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.deattach_interface_lag]")

    @staticmethod
    async def attach_interface_lag(interface_id: str, lag_id: str) -> CustomResponse:
        """
        Method responsible for attach a interface lag
        """

        logger.info("Facade: Attach interface lag...")
        try:
            find_interface = await InterfaceSingleSchema.get(ObjectId(interface_id), fetch_links=True)
            if find_interface is None:
                logger.error("Interface  %s not found!", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format("Interface  ", interface_id))

            find_lag = await InterfaceLagSchema.get(ObjectId(lag_id), fetch_links=True)
            find_interface.lag = find_lag
            find_interface.ipaddr = None
            find_interface.type = "lag"
            find_interface.mode = "unknown"
            find_interface.vrf = None
            find_interface.vlan = None
            await find_interface.save()

            logger.info("Facade: Attach interface lag success: %s", find_lag.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, find_lag.name), data=find_lag)

        except DuplicateKeyError as err:
            logger.error("Error attach interface lag (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, find_lag.name))

        except Exception as err:
            logger.error("Error attach interface lag (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.attach_interface_lag]")

    @staticmethod
    async def update_interface_lag(interface_id: str, interface: Type[InterfaceLagBase]) -> CustomResponse:
        """
        Method responsible for update a interface lag
        """

        logger.info("Facade: Update interface lag...")
        try:
            find_interface_lag = await InterfaceLagSchema.get(interface_id)
            if find_interface_lag is None:
                logger.error("Interface lag %s not found! [update]", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, interface_id))

            logger.info("Facade: find interface lag success [update]: %s", find_interface_lag.dict())
            for field, value in interface.model_dump(exclude_unset=True).items():
                setattr(find_interface_lag, field, value)

            update_interface_lag = await find_interface_lag.replace()
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, interface.name), data=update_interface_lag)

        except DuplicateKeyError as err:
            logger.error("Error update interface lag (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, interface.name))

        except Exception as err:
            logger.error("Error update interface lag (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.update_interface_lag]")

    @staticmethod
    async def get_interface_lags() -> CustomResponse:
        """
        Method responsible for get all interface lags
        """

        logger.info("Facade: Get all interface lags...")
        try:
            interface_lags = await InterfaceLagSchema.find(fetch_links=True, nesting_depth=2).to_list()
            return CustomResponse.success(message=FOUND.format(operation), data=interface_lags)

        except Exception as err:
            logger.error("Error get all interface lags (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.get_interface_lags]")

    @staticmethod
    async def get_interface_lags_by_device_id(device_id: str) -> CustomResponse:
        """
        Method responsible for get all interface lags by device id
        """

        logger.info("Facade: Get all interface lags device id...")
        try:
            interface_lags = await InterfaceLagSchema.find(
                {"interface.device._id": ObjectId(device_id)  }, fetch_links=True, nesting_depth=2
            ).to_list()

            return CustomResponse.success(message=FOUND.format(operation), data=interface_lags)

        except Exception as err:
            logger.error("Error get all interface lags (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.get_interface_lags]")

    @staticmethod
    async def delete_interface_lag(interface_id: str) -> CustomResponse:
        """
        Method responsible for delete a interface lag
        """

        logger.info("Facade: Delete interface lag...")
        try:
            interface_lag = await InterfaceLagSchema.get(interface_id)
            if interface_lag is None:
                logger.error("Interface lag %s not found!", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, interface_id))

            await interface_lag.delete()
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, interface_lag.name))

        except Exception as err:
            logger.error("Error delete interface lag (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceLagFacade.delete_interface_lag]")
