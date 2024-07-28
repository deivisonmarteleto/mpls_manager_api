"""
Module responsible for the location facade
"""
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.core.facilities.locations.models import LocationsBase
from src.app.core.facilities.locations.schema import LocationsSchema
from src.app.core.ipam.l2domain.schema import L2DomainSchema
from src.app.shared.messages import ALREADY_EXISTS, FOUND, NOT_FOUND, UPDATE_SUCCESS, CREATE_SUCCESS, DELETE_SUCCESS
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)

operation = "location"

class LocationsFacade:
    """
    Class responsible for the facade  locations
    """

    @staticmethod
    async def create_location(location: LocationsBase) -> CustomResponse:
        """
        Method responsible for creating a locations
        """

        logger.info("Facade: Creating  Locations...")
        try:
            create_location = await LocationsSchema(**location.model_dump(exclude_unset=True)).insert()
            logger.info("Facade: Creating  Locations success: %s", create_location.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, create_location.name), data=create_location)

        except DuplicateKeyError as err:
            logger.error("Error creating locations (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, location.name))

        except Exception as err:
            logger.error("Error creating location (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [LocationsFacade.create_locations]")

    @staticmethod
    async def update_location(location_id: str, location: LocationsBase) -> CustomResponse:
        """
        Method responsible for update a Locations
        """

        logger.info("Facade: Update location: %s", location_id)
        try:
            find_location = await LocationsSchema.get(location_id)
            if find_location is None:
                logger.error("Facade: Update Location %s not found!", location_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, location_id))

            logger.info("Facade: find location success [update]: %s", find_location.dict())

            for field, value in location.model_dump(exclude_unset=True).items():
                if field in  ["id", "_id"]:
                    continue

                current_value = getattr(find_location, field)

                if value != current_value or (value is None and current_value is not None):
                    logger.info("Facade: Update location field: %s", field)
                    setattr(find_location, field, value)

            await find_location.save()

            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, find_location.name), data=find_location)

        except DuplicateKeyError as err:
            logger.error("Error update Location (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, location.name))

        except Exception as err:
            logger.error("Error update Location (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [LocationsFacade.update_location]")

    @staticmethod
    async def get_location() -> CustomResponse:
        """
        Method responsible for getting all location
        """
        logger.info("Getting all location...")
        get_location = await LocationsSchema.find(fetch_links=True).to_list()
        if len(get_location) == 0:
            logger.error("Location not found!")
        else:
            logger.info("Facade: Location get all successfully: %s", len(get_location))

        return CustomResponse.success(message=FOUND.format(operation), data=get_location)

    @staticmethod
    async def get_location_by_id(location_id: str) -> CustomResponse:
        """
        Method responsible for getting all location by id
        """
        logger.info("Getting location by id...")
        get_location = await LocationsSchema.get(location_id,fetch_links=True)
        if get_location is None:
            logger.error("Location not found! (get_location_by_id)")
            return CustomResponse.failure(message=NOT_FOUND.format(operation, location_id))

        logger.info("Facade: Location get all successfully: %s", get_location.dict())
        return CustomResponse.success(message=FOUND.format(operation), data=get_location)

    @staticmethod
    async def get_location_by_group_name(group_name: str) -> CustomResponse:
        """
        Method responsible for getting all location by group name
        """
        logger.info("Getting all location by group name...")
        get_location = await LocationsSchema.find(LocationsSchema.group.name ==  group_name, fetch_links=True).to_list()
        if len(get_location) == 0:
            logger.error("Location by group name not found!")
        else:
            logger.info("Facade: Location get all by group name successfully: %s", len(get_location))

        return CustomResponse.success(message=FOUND.format(operation), data=get_location)

    @staticmethod
    async def delete_location(location_id: str) -> CustomResponse:
        """
        Method responsible for deleting a location by id
        """
        logger.info("Facade: Starting Deleting location: %s", location_id)
        delete_location = await LocationsSchema.get(location_id)
        if delete_location is None:
            logger.error("Facade: Location %s not found! [delete]", location_id)
            return CustomResponse.failure(message=NOT_FOUND.format(location_id))

        # find_rack = await RackSchema.find(
        #     RackSchema.location.id == ObjectId(delete_location.id)
        # ).count()
        # if find_rack > 0:
        #     logger.error("Facade: Location %s has racks associated with it!", location_id)
        #     return CustomResponse.failure(message="Localização %s possui racks associados a ela!" % delete_location.name)

        # find_l2domain = await L2DomainSchema.find(
        #     L2DomainSchema.location.id == ObjectId(delete_location.id)
        # ).count()
        # if find_l2domain > 0:
        #     logger.error("Facade: Location %s has L2Domain associated with it!", location_id)
        #     return CustomResponse.failure(message="Localização %s possui L2Domain associados a ela!" % delete_location.name)

        await delete_location.delete()
        return CustomResponse.success(message=DELETE_SUCCESS.format(operation, delete_location.name))
