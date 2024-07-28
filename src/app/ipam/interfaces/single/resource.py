"""
Module for single resource interfaces
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.ipam.interfaces.single.models import InterfaceSingleBase
from src.app.ipam.interfaces.single.facade import InterfaceSingleFacade

from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger


logger = get_logger(__name__)


router = APIRouter(
    prefix="/ipam",
    tags=["interfaces_single"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)


@router.get("/interface_single/device/{device_id}")
async def get_interface_single_by_device(device_id: str):
    """
    Method responsible for get a interface_single by device id
    """
    logger.info("Resource: Starting interface_single get by device id")
    get_interface_single = await InterfaceSingleFacade.get_interface_single_by_device(device_id=device_id)
    if get_interface_single["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_interface_single["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_interface_single["message"] )


@router.post("/interface_single/{device_id}")
async def post_create_interface_single(interface: InterfaceSingleBase, device_id: str):
    """
    Method responsible for creating a interface_single
    """
    logger.info("Resource: Starting interface_single creation: %s", interface)

    create_interface_single = await InterfaceSingleFacade.create_interface_single(interface=interface, device_id=device_id )
    if create_interface_single["status"] == "success":
        logger.info("interface_single was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_interface_single["data"]) )

    logger.error("interface_single was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_interface_single["message"] )


@router.put("/interface_single/{interface_id}")
async def put_interface_single(interface_id: str, interface: InterfaceSingleBase):
    """
    Method responsible for update a interface_single
    """
    logger.info("Resource: Starting interface_single update: %s", interface.dict())

    update_interface_single = await InterfaceSingleFacade.update_interface_single(interface_id=interface_id, interface=interface)
    if update_interface_single["status"] == "success":
        logger.info("interface_single was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_interface_single["data"]) )

    logger.error("interface_single was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_interface_single["message"] )


@router.get("/interface_single")
async def get_interface_singles():
    """
    Method responsible for listing all interface_single
    """
    logger.info("Resource: Starting interface_single get all")

    get_interface_single = await InterfaceSingleFacade.get_interface_singles()
    if get_interface_single["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_interface_single["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_interface_single["message"] )


@router.get("/interface_single/{interface_id}")
async def get_interface_single(interface_id: str):
    """
    Method responsible for get a interface_single by id
    """
    logger.info("Resource: Starting interface_single get by id")
    get_interface_single = await InterfaceSingleFacade.get_interface_single(interface_id=interface_id)
    if get_interface_single["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_interface_single["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_interface_single["message"] )


@router.delete("/interface_single/{interface_id}")
async def delete_interface_single(interface_id: str):
    """
    Method responsible for delete a interface_single
    """
    logger.info("Resource: Starting interface_single delete by id")
    delete_interface_single = await InterfaceSingleFacade.delete_interface_single(interface_id=interface_id)
    if delete_interface_single["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=delete_interface_single["data"])

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=delete_interface_single["message"])
