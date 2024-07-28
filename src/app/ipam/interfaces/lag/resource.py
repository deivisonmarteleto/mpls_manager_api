"""
Module responsible for interface lag routes
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.ipam.interfaces.lag.models import InterfaceLagBase
from src.app.ipam.interfaces.lag.facade import InterfaceLagFacade

from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger


logger = get_logger(__name__)


router = APIRouter(
    prefix="/ipam",
    tags=["interfaces_lag"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)


@router.post("/interface_lag/interface_single/{interface_id}")
async def post_create_interface_lag(interface: InterfaceLagBase, interface_id: str):
    """
    Method responsible for creating a interface_lag
    """
    logger.info("Resource: Starting interface_lag creation: %s", interface)

    create_interface_lag = await InterfaceLagFacade.create_interface_lag(interface=interface, interface_id=interface_id)
    if create_interface_lag["status"] == "success":
        logger.info("interface_lag was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_interface_lag["data"]) )

    logger.error("interface_lag was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_interface_lag["message"] )

@router.put("/interface_lag/{interface_id}")
async def put_interface_lag(interface_id: str, interface: InterfaceLagBase):
    """
    Method responsible for update a interface_lag
    """
    logger.info("Resource: Starting interface_lag update: %s", interface.dict())

    update_interface_lag = await InterfaceLagFacade.update_interface_lag(interface_id=interface_id, interface=interface)
    if update_interface_lag["status"] == "success":
        logger.info("interface_lag was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_interface_lag["data"]) )

    logger.error("interface_lag was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_interface_lag["message"] )

@router.put("/interface_lag/attach/{interface_id}/{lag_id}")
async def put_interface_lag_attach(interface_id: str, lag_id: str):
    """
    Method responsible for attach a interface_lag
    """
    logger.info("Resource: Starting interface_lag attach: %s", interface_id)

    attach_interface_lag = await InterfaceLagFacade.attach_interface_lag(interface_id=interface_id, lag_id=lag_id)
    if attach_interface_lag["status"] == "success":
        logger.info("interface_lag was attach successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(attach_interface_lag["data"]) )

    logger.error("interface_lag was not attach. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=attach_interface_lag["message"] )

@router.put("/interface_lag/detach/{interface_id}")
async def put_interface_lag_detach(interface_id: str):
    """
    Method responsible for detach a interface_lag
    """
    logger.info("Resource: Starting interface_lag detach: %s", interface_id)

    detach_interface_lag = await InterfaceLagFacade.detach_interface_lag(interface_id=interface_id)
    if detach_interface_lag["status"] == "success":
        logger.info("interface_lag was detach successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(detach_interface_lag["data"]) )

    logger.error("interface_lag was not detach. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=detach_interface_lag["message"])


@router.get("/interface_lag/device/{device_id}")
async def get_interface_lag_by_device_id(device_id: str):
    """
    Method responsible for listing all interface_lag by device_id
    """
    logger.info("Resource: Starting interface_lag get by device_id: %s", device_id)

    get_interface_lags = await InterfaceLagFacade.get_interface_lags_by_device_id(device_id=device_id)
    if get_interface_lags["status"] == "success":
        logger.info("interface_lag was get successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_interface_lags["data"]) )

    logger.error("interface_lag was not get. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_interface_lags["message"] )


@router.get("/interface_lag")
async def get_interface_lags():
    """
    Method responsible for listing all interface_lag
    """
    logger.info("Resource: Starting interface_lag get all")

    get_interface_lags = await InterfaceLagFacade.get_interface_lags()
    if get_interface_lags["status"] == "success":
        logger.info("interface_lag was get successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_interface_lags["data"]) )

    logger.error("interface_lag was not get. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_interface_lags["message"] )


@router.delete("/interface_lag/{interface_id}")
async def delete_interface_lag(interface_id: str):
    """
    Method responsible for delete a interface_lag
    """
    logger.info("Resource: Starting interface_lag delete by id: %s", interface_id)
    delete_interface_lag = await InterfaceLagFacade.delete_interface_lag(interface_id=interface_id)
    if delete_interface_lag["status"] == "success":
        logger.info("interface_lag was deleted successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=delete_interface_lag["message"] )

    logger.error("interface_lag was not deleted. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=delete_interface_lag["message"] )
