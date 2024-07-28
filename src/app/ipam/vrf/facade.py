"""
Module responsible for vrf Facade
"""

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from typing import Type

from src.app.core.ipam.vrf.models import VrfBase
from src.app.core.ipam.vrf.schema import VrfSchema
from src.app.shared.messages import ALREADY_EXISTS, FOUND, NOT_FOUND, UPDATE_SUCCESS, CREATE_SUCCESS, DELETE_SUCCESS
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)

operation = "vrf"

class VrfFacade:
    """
    Class responsible for the facade of the vrf
    """

    @staticmethod
    async def create_vrf(vrf: Type[VrfBase]) -> CustomResponse:
        """
        Method responsible for creating vrf
        """

        logger.info("Facade: Creating vrf...")
        try:

            create_vrf = await VrfSchema(**vrf.model_dump(exclude_unset=True)).insert()
            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, vrf.name), data=create_vrf)

        except DuplicateKeyError as err:
            logger.error("Error creating vrf (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, vrf.name))

        except Exception as err:
            logger.error("Error creating vrf (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VrfFacade.create_vrf]")

    @staticmethod
    async def update_vrf(vrf_id: str, vrf: Type[VrfBase]) -> CustomResponse:
        """
        Method responsible for update a vrf
        """

        logger.info("Facade: Update vrf...")
        try:
            find_vrf = await VrfSchema.get(vrf_id)
            if find_vrf is None:
                logger.error("Vrf %s not found! [update]", vrf_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, vrf_id))

            logger.info("Facade: find vrf success [update]: %s", find_vrf.dict())
            for field, value in vrf.model_dump(exclude_unset=True).items():
                setattr(find_vrf, field, value)

            update_vrf = await find_vrf.replace()
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, vrf.name), data=update_vrf)

        except DuplicateKeyError as err:
            logger.error("Error update vrf (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, vrf.name))

        except Exception as err:
            logger.error("Error update vrf(Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VrfFacade.update_vrf]")

    @staticmethod
    async def get_vrfs() -> CustomResponse:
        """
        Method responsible for get all vrfs
        """
        logger.info("Facade: Get all vrfs...")
        try:
            vrfs = await VrfSchema.get_all()
            return CustomResponse.success(message=FOUND.format(operation), data=vrfs)

        except Exception as err:
            logger.error("Error get all vrfs (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VrfFacade.get_vrfs]")

    @staticmethod
    async def get_vrf(vrf_id: str) -> CustomResponse:
        """
        Method responsible for get a vrf
        """

        logger.info("Facade: Get vrf...")
        try:
            find_vrf = await VrfSchema.get(vrf_id)
            if find_vrf is None:
                logger.error("Vrf %s not found!", vrf_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, vrf_id))

            return CustomResponse.success(message=FOUND.format(operation), data=find_vrf)

        except Exception as err:
            logger.error("Error get vrf (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VrfFacade.get_vrf]")

    @staticmethod
    async def delete_vrf(vrf_id: str) -> CustomResponse:
        """
        Method responsible for delete a vrf
        """

        logger.info("Facade: Delete vrf...")
        try:
            find_vrf = await VrfSchema.get(vrf_id)
            if find_vrf is None:
                logger.error("Vrf %s not found!", vrf_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, vrf_id))

            await find_vrf.delete()
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, find_vrf.name))

        except Exception as err:
            logger.error("Error delete vrf (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VrfFacade.delete_vrf]")
