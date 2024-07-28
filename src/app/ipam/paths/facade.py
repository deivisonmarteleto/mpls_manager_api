"""
Module responsible for facade paths
"""



from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import  DeleteRules

from src.app.core.ipam.devices.schema import DevicesSchema
from src.app.core.ipam.paths.models import PathsBase
from src.app.core.ipam.paths.schema import PathsSchema
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)


operation = "path"

class PathFacade:
    """
    Class responsible for the facade of the path
    """

    @staticmethod
    async def get_paths() -> CustomResponse:
        """
        Method responsible for get all paths
        """

        logger.info("Facade: Get all paths...")
        try:
            paths = await PathsSchema.find(fetch_links=True, nesting_depth=1).to_list()
            logger.info("Facade: Get all paths success: %s", paths)
            return CustomResponse.success(message=FOUND.format(operation), data=paths)
        except Exception as err:
            logger.error("Error get all paths (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [PathFacade.get_paths]")

    @staticmethod
    async def create_path(path: Type[PathsBase]) -> CustomResponse:
        """
        Method responsible for creating path
        """

        logger.info("Facade: Creating path...")
        try:
            add_prefix = "PATH-" + path.name
            path.name = add_prefix.upper()
            path.created_at = datetime.now().isoformat()
            create_path = PathsSchema(**path.model_dump(exclude_unset=True))
            await create_path.insert()

            logger.info("Facade: Creating path success: %s", create_path.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, path.name), data=create_path)

        except DuplicateKeyError as err:
            logger.error("Error creating path (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, path.name))

        except Exception as err:
            logger.error("Error creating path (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [PathFacade.create_path]")

    @staticmethod
    async def update_path(path_id: str, path: Type[PathsBase]) -> CustomResponse:
        """
        Method responsible for update a path
        """

        logger.info("Facade: Update path...")
        try:
            find_path = await PathsSchema.find_one(PathsSchema.id == ObjectId(path_id), fetch_links=True)
            if find_path is None:
                logger.error("Path %s not found! [update]", path_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, path_id))

            logger.info("Facade: find path success [update]: %s", find_path.dict())
            for field, value in path.model_dump(exclude_unset=True).items():
                if field in  ["id", "_id"]:
                    continue
                current_value = getattr(find_path, field)

                if value != current_value or (value is None and current_value is not None):
                    logger.info("Facade: Update tunnel field: %s", field)
                    setattr(find_path, field, value)

            await find_path.save()
            logger.info("Facade: Update path success...")
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, path.name), data=find_path)

        except Exception as err:
            logger.error("Error update path (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [PathFacade.update_path]")

    @staticmethod
    async def delete_path(path_id: str) -> CustomResponse:
        """
        Method responsible for delete a path
        """

        logger.info("Facade: Delete path...")
        try:
            find_path = await PathsSchema.get(ObjectId(path_id), fetch_links=True)
            if find_path is None:
                logger.error("Path %s not found!", path_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, path_id))

            await find_path.delete()
            logger.info("Facade: Delete path success...")
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, find_path.name))
        except Exception as err:
            logger.error("Error delete path (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [PathFacade.delete_path]")

    @staticmethod
    async def get_path_by_device(device_id: str) -> CustomResponse:
        """
        Method responsible for get all paths by device id
        """

        logger.info("Facade: Get all paths by device id...")
        try:
            paths = await PathsSchema.find(
                {"step_1._id": ObjectId(device_id)  }, fetch_links=True
            ).to_list()

            return CustomResponse.success(message=FOUND.format(operation), data=paths)

        except Exception as err:
            logger.error("Error get all paths (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [PathFacade.get_paths]")
