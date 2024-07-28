"""
Module responsible for devices olt  routes
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.ipam.devices.models import DevicesBase

from src.app.ipam.devices.facade import DevicesFacade

from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix="/ipam",
    tags=["devices"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/device")
async def post_create_device(device: DevicesBase):
    """
    Method responsible for creating a device
    """
    logger.info("Resource: Starting device creation: %s", device)

    create_device = await DevicesFacade.create_device(device=device)
    if create_device["status"] == "success":
        logger.info("Device was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_device["data"]) )

    logger.error("Device was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_device["message"] )

@router.put("/device/{device_id}")
async def put_device(device_id: str, device: DevicesBase):
    """
    Method responsible for update a device
    """
    logger.info("Resource: Starting device update: %s", device.dict())

    update_device = await DevicesFacade.update_device(device_id=device_id, device=device)
    if update_device["status"] == "success":
        logger.info("Device was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_device["data"]) )

    logger.error("Device was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_device["message"] )

@router.get("/device")
async def get_devices():
    """
    Method responsible for listing all devices
    """
    logger.info("Resource: Starting devices get all")

    get_device = await DevicesFacade.get_devices()
    if get_device["status"] == "success":
        logger.info("Device was get successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(get_device["data"]) )

    logger.error("Device was not get. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_device["message"] )

@router.get("/device/{device_id}")
async def get_device_by_id(device_id: str):
    """
    Method responsible for get a device by id
    """
    logger.info("Resource: Starting device get by id: %s", device_id)

    get_device = await DevicesFacade.get_device_by_id(device_id=device_id)
    if get_device["status"] == "success":
        logger.info("Device was get successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(get_device["data"]) )

    logger.error("Device was not get. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_device["message"] )

@router.delete("/device/{device_id}", response_model=str)
async def delete_device(device_id: str):
    """
    Method responsible for delete a device
    """
    logger.info("Resource: Starting drop device id: %s", device_id)

    remove_device = await DevicesFacade.delete_device(device_id=device_id)
    if remove_device["status"] == "success":
        logger.info("Device was deleted successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_device["message"] )

    logger.error("Device was not deleted. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_device["message"] )
