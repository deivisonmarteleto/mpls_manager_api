"""
Module responsible for the vendor facade
"""
from pymongo.errors import DuplicateKeyError

from src.app.core.facilities.vendors.models import VendorBase
from src.app.core.facilities.vendors.schema import VendorSchema
from src.app.shared.response import CustomResponse
from src.logging import get_logger
from src.app.shared.messages import ALREADY_EXISTS, NOT_FOUND,CREATE_SUCCESS, UPDATE_SUCCESS, FOUND, DELETE_SUCCESS

logger = get_logger(__name__)

operation = "vendor"

class VendorFacade:
    """
    Class responsible for the facade of the vendor
    """

    @staticmethod
    async def create_vendor(vendor: VendorBase) -> CustomResponse:
        """
        Method responsible for creating vendor
        """

        logger.info("Facade: Creating vendor...")
        try:

            create_vendor = await VendorSchema(**vendor.model_dump(exclude_unset=True)).insert()
            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, vendor.name), data=create_vendor)

        except DuplicateKeyError as err:
            logger.error("Error creating vendor (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, vendor.name))

        except Exception as err:
            logger.error("Error creating vendor (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VendorFacade.create_vendor]")

    @staticmethod
    async def update_vendor(vendor_id: str, vendor: VendorBase) -> CustomResponse:
        """
        Method responsible for update a vendor
        """

        logger.info("Facade: Update vendor...")
        try:
            find_vendor = await VendorSchema.get(vendor_id)
            if find_vendor is None:
                logger.error("Vendor %s not found! [update]", vendor_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, vendor_id))

            logger.info("Facade: find vendor success [update]: %s", find_vendor.dict())
            for field, value in vendor.model_dump(exclude_unset=True).items():
                if field in  ["id", "_id"]:
                    continue
                current_value = getattr(find_vendor, field)

                if value != current_value or (value is None and current_value is not None):
                    logger.info("Facade: Update vendor field: %s", field)
                    setattr(find_vendor, field, value)

            await find_vendor.replace()
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, vendor.name), data=find_vendor)

        except DuplicateKeyError as err:
            logger.error("Error update vendor (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message="Nome %s está em uso..." % vendor.name)

        except Exception as err:
            logger.error("Error update vendor (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VendorFacade.update_vendor]")

    @staticmethod
    async def get_vendors() -> CustomResponse:
        """
        Method responsible for getting a vendor
        """
        logger.info("Getting all vendors...")
        get_vendors = await VendorSchema.find(fetch_links=True).to_list()
        if len(get_vendors) == 0:
            logger.error("Vendors not found!")
        else:
            logger.info("Vendors found: %s", len(get_vendors))
        return CustomResponse.success(message=FOUND.format(operation), data=get_vendors)

    @staticmethod
    async def delete_vendor(vendor_id: str) -> CustomResponse:
        """
        Method responsible for deleting a vendor
        """
        logger.info("Facade: Deleting vendor...")
        delete_vendor = await VendorSchema.get(vendor_id)
        if delete_vendor is None:
            logger.error("Vendor %s not found! [delete]", vendor_id)
            return CustomResponse.failure(message=NOT_FOUND.format(operation ,vendor_id))

        # find_olt = await ChassisOltSchema.find(ChassisOltSchema.vendor.id == delete_vendor.id, fetch_links=True).to_list()
        # if len(find_olt) > 0:
        #     logger.error("Vendor %s is being used by OLTs!", vendor_id)
        #     return CustomResponse.failure(message="Fabricante %s possui OLTs associadas." % delete_vendor.name)

        await delete_vendor.delete()
        return CustomResponse.success(message=DELETE_SUCCESS.format(operation, vendor_id), data=delete_vendor)
