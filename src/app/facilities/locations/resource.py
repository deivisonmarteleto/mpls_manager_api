"""
Module responsible for group locations routes
"""
from time import sleep
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.facilities.locations.models import LocationsBase
from src.app.facilities.locations.facade import LocationsFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/facilities",
    tags=["location"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/location")
async def post_location(location: LocationsBase):
    """
    Method route responsible for creating a Location
    """
    logger.info("Resource: Starting location creation: %s", location.dict())
    create_location = await LocationsFacade.create_location(location=location)
    if create_location["status"] == "success":
        logger.info("Location was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_location["data"]) )

    logger.error("Location was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_location["message"] )

@router.put("/location/{location_id}")
async def put_location(location_id: str, location: LocationsBase):
    """
    Method route responsible for update a location
    """
    logger.info("Resource: Starting location update: %s", location.dict())

    update_location = await LocationsFacade.update_location(location_id=location_id, location=location)
    if update_location["status"] == "success":
        logger.info("Location was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_location["data"]) )

    logger.error("Location was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_location["message"] )

@router.get("/location")
async def get_location():
    """
    Method route responsible for listing all group_location
    """
    logger.info("Resource: Starting group_location get all")
    get_locations = await LocationsFacade.get_location()
    if get_locations["status"] == "success":
        logger.info(" Location get all successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_locations["data"]))

    logger.error("Location get all failed. FIM!")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=get_locations["message"])

@router.get("/location/{group_name}")
async def get_location_by_group_name(group_name: str):
    """
    Method route responsible for listing all location by group name
    """
    logger.info("Resource: Starting location get all by group name: %s", group_name)

    get_locations = await LocationsFacade.get_location_by_group_name(group_name=group_name)
    if get_locations["status"] == "success":
        logger.info(" Location get all by group name successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_locations["data"]))

    logger.error("Location get all failed by group name. FIM!")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=get_locations["message"])

@router.delete("/location/{location_id}", response_model=str)
async def delete_group_location(location_id: str):
    """
    Method route responsible for delete a  location
    """
    logger.info("Resource: Starting drop location id: %s", location_id)

    remove_location = await LocationsFacade.delete_location(location_id=location_id)
    if remove_location["status"] == "success":
        logger.info("Location was deleted successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_location["message"] )

    logger.error("Location was not deleted. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_location["message"] )
