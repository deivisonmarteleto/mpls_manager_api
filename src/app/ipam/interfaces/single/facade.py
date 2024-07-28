"""
module for single facility interface
"""

from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import  DeleteRules

from src.app.core.ipam.devices.schema import DevicesSchema
from src.app.core.ipam.interfaces.single.models import \
    InterfaceSingleBase
from src.app.core.ipam.interfaces.single.schema import \
    InterfaceSingleSchema
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)


operation = "interface single"


class InterfaceSingleFacade:
    """
    Class responsible for the facade of the interface single
    """

    @staticmethod
    async def get_interface_single_by_device(device_id: str) -> CustomResponse:
        """
        Method responsible for get a interface single by device id
        """

        logger.info("Facade: Get interface single by device id...")
        try:
            find_device = await DevicesSchema.get(ObjectId(device_id), fetch_links=True)
            if find_device is None:
                logger.error("Device %s not found!", device_id)
                return CustomResponse.failure(message=NOT_FOUND.format("device", device_id))

            logger.info("Facade: find device success: %s", find_device.dict())

            find_interface_single = await InterfaceSingleSchema.find(
                InterfaceSingleSchema.device.id == find_device.id, fetch_links=True, nesting_depth=1
            ).to_list()

            logger.info("Facade: Get interface single by device id success: %s", find_interface_single)
            return CustomResponse.success(message=FOUND.format(operation), data=find_interface_single)

        except Exception as err:
            logger.error("Error get interface single by device id (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceSingleFacade.get_interface_single_by_device]")

    @staticmethod
    async def create_interface_single(interface: Type[InterfaceSingleBase], device_id: str) -> CustomResponse:
        """
        Method responsible for creating interface single
        """

        logger.info("Facade: Creating interface single...")
        try:
            find_device = await DevicesSchema.get(ObjectId(device_id), fetch_links=True)
            if find_device is None:
                logger.error("Device %s not found!", device_id)
                return CustomResponse.failure(message=NOT_FOUND.format("device", device_id))

            logger.info("Facade: find device success: %s", find_device.dict())

            create_interface_single =  InterfaceSingleSchema(**interface.model_dump(exclude_unset=True))
            create_interface_single.device = find_device
            await create_interface_single.insert()

            logger.info("Facade: Creating interface single success: %s", create_interface_single.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, interface.name), data=create_interface_single)

        except DuplicateKeyError as err:
            logger.error("Error creating interface single (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, interface.name))

        except Exception as err:
            logger.error("Error creating interface single (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceSingleFacade.create_interface_single]")

    @staticmethod
    async def update_interface_single(interface_id: str, interface: Type[InterfaceSingleBase]) -> CustomResponse:
        """
        Method responsible for update a interface single
        """

        logger.info("Facade: Update interface single...")
        try:
            find_interface_single = await InterfaceSingleSchema.get(interface_id)
            if find_interface_single is None:
                logger.error("Interface single %s not found! [update]", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, interface_id))

            logger.info("Facade: find interface single success [update]: %s", find_interface_single.dict())
            for field, value in interface.model_dump(exclude_unset=True).items():
                setattr(find_interface_single, field, value)

            update_interface_single = await find_interface_single.replace()
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, interface.name), data=update_interface_single)

        except DuplicateKeyError as err:
            logger.error("Error update interface single (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, interface.name))

        except Exception as err:
            logger.error("Error update interface single (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceSingleFacade.update_interface_single]")

    @staticmethod
    async def get_interface_singles() -> CustomResponse:
        """
        Method responsible for get all interface single
        """

        logger.info("Facade: Get all interface single...")
        try:
            get_interface_single = await InterfaceSingleSchema.find(fetch_links=True, nesting_depth=1).to_list()
            logger.info("Facade: Get all interface single success: %s", get_interface_single)
            return CustomResponse.success(message=FOUND.format(operation), data=get_interface_single)

        except Exception as err:
            logger.error("Error get all interface single (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceSingleFacade.get_interface_singles]")

    @staticmethod
    async def get_interface_single(interface_id: str) -> CustomResponse:
        """
        Method responsible for get a interface single
        """

        logger.info("Facade: Get interface single: %s", interface_id)
        try:
            find_interface_single = await InterfaceSingleSchema.find_one(InterfaceSingleSchema.id == ObjectId(interface_id), fetch_links=True )
            if find_interface_single is None:
                logger.error("Interface single %s not found!", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, interface_id))


            return CustomResponse.success(message=FOUND.format(operation), data=find_interface_single)

        except Exception as err:
            logger.error("Error get interface single (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceSingleFacade.get_interface_single]")

    @staticmethod
    async def delete_interface_single(interface_id: str) -> CustomResponse:
        """
        Method responsible for delete a interface single
        """

        logger.info("Facade: Delete interface single...")
        try:
            find_interface_single =  await InterfaceSingleSchema.get(ObjectId(interface_id) )
            if find_interface_single is None:
                logger.error("Interface single %s not found!", interface_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, interface_id))

            logger.info("Facade: find interface single success: %s", find_interface_single.dict())

            teste = await find_interface_single.delete(link_rule=DeleteRules.DELETE_LINKS)
            logger.info("Facade: Delete interface single success: %s", teste)
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, interface_id), data=interface_id)

        except Exception as err:
            logger.error("Error delete interface single (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [InterfaceSingleFacade.delete_interface_single]")
