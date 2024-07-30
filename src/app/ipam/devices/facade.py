"""
Module responsible for the ipam  chassis olt facade
"""
from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie.operators import Set
from beanie.odm.fields import  DeleteRules


from src.app.core.ipam.devices.models import DevicesBase
from src.app.core.ipam.devices.schema import DevicesSchema
from src.app.core.facilities.locations.schema import LocationsSchema
from src.app.core.facilities.vendors.schema import VendorSchema
from src.app.shared.messages import ALREADY_EXISTS, FOUND, NOT_FOUND, UPDATE_SUCCESS, CREATE_SUCCESS, DELETE_SUCCESS
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)



operation = "devices"
operation = "Ip Address"

class DevicesFacade:
    """
    Class responsible for the facade of the devices
    """

    @staticmethod
    async def create_device(device: Type[DevicesBase]) -> CustomResponse:
        """
        Method responsible for creating device
        """

        logger.info("Facade: Creating device...")
        try:
            device.created_at = datetime.now().isoformat()
            ipaddr = device.ipaddr.split("/")
            check_ipaddr = await DevicesSchema.find().to_list()
            for ip in check_ipaddr:
                if ipaddr[0] == ip.ipaddr.split("/")[0]:
                    return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, ip.ipaddr.split("/")[0]))

            create_device = await DevicesSchema(**device.model_dump(exclude_unset=True)).insert()

            logger.info("Facade: Creating device success: %s", create_device.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, device.name), data=create_device)

        except DuplicateKeyError as err:
            logger.error("Error creating device (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, device.name))

        except Exception as err:
            logger.error("Error creating device (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [DevicesFacade.create_device]")

    @staticmethod
    async def update_device(device_id: str, device: Type[DevicesBase]) -> CustomResponse:
        """
        Method responsible for update a device
        """

        logger.info("Facade: Update device...")
        try:
            find_device = await DevicesSchema.find_one(DevicesSchema.id == ObjectId(device_id), fetch_links=True)
            if find_device is None:
                logger.error("Device %s not found! [update]", device_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, device_id))

            logger.info("Facade: find device success [update]: %s", find_device.dict())
            for field, value in device.model_dump(exclude_unset=True).items():

                if field == "location":
                    logger.info("select location update (update_device)....")

                    find_location = await LocationsSchema.get(ObjectId(value))
                    if find_location is None:
                        return CustomResponse.failure(message=NOT_FOUND.format("location", value))

                    setattr(find_device, field, find_location)
                    logger.info("Location update success (update_device): %s", find_device)
                    continue

                if field == "vendor":
                    logger.info("select vendor update (update_device)....")

                    find_vendor = await VendorSchema.get(ObjectId(value))
                    if find_vendor is None:
                        return CustomResponse.failure(message=NOT_FOUND.format("vendor", value))

                    setattr(find_device, field, find_vendor)
                    logger.info("Vendor update success (update_device): %s", find_device)
                    continue

                setattr(find_device, field, value)

            update_device = await find_device.save()
            logger.info("Facade: Update device success...")
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, device.name), data=update_device)


        except DuplicateKeyError as err:
            logger.error("Error update device (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, device.name))

        # except Exception as err:
        #     logger.error("Error update device (Exception): %s", err)
        #     return CustomResponse.failure(message="Interno error: [DevicesFacade.update_device]")

    @staticmethod
    async def get_devices() -> CustomResponse:
        """
        Method responsible for getting all devices
        """
        logger.info("Getting all devices...")
        get_devices = await DevicesSchema.find(fetch_links=True, nesting_depth=2).to_list()

        # if len(get_devices) == 0:
        #     logger.error("Devices not found!")
        #     return CustomResponse.failure(message=NOT_FOUND.format(operation, "devices"))

        logger.info("Devices found successfully . FIM! - %s", get_devices)
        return CustomResponse.success(message=FOUND.format(operation), data=get_devices)

    @staticmethod
    async def get_device_by_id(device_id: str) -> CustomResponse:
        """
        Method responsible for getting a device by id
        """
        logger.info("Getting device by id...")
        get_device = await DevicesSchema.get(device_id)
        if get_device is None:
            logger.error("Device not found! (get_device_by_id)")
            return CustomResponse.failure(message=NOT_FOUND.format(operation, device_id))

        logger.info("Device found successfully . FIM! - %s", get_device.dict())
        return CustomResponse.success(message=FOUND.format(operation), data=get_device)

    @staticmethod
    async def delete_device(device_id: str) -> CustomResponse:
        """
        Method responsible for deleting a device
        """
        logger.info("Facade: Deleting device: %s", device_id)

        delete_device = await DevicesSchema.get(device_id, fetch_links=True)
        if delete_device is None:
            logger.error("Device %s not found! (delete_device)", device_id)
            return CustomResponse.failure(message=NOT_FOUND.format(operation, device_id))

        delete_device.location = None
        delete_device.vendor = None


        await delete_device.save()
        logger.info("Facade: Deleting device: %s", delete_device.id)
        await delete_device.delete(link_rule=DeleteRules.DELETE_LINKS)
        return CustomResponse.success(message=DELETE_SUCCESS.format(operation, delete_device.name), data=delete_device.id)
