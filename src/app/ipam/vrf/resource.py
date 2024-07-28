"""
Module responsible for vrf rote
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.ipam.vrf.models import VrfBase
from src.app.ipam.vrf.facade import VrfFacade
from src.app.shared.serialize import SerializationFilter
from src.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ipam",
    tags=["vrf"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/vrf")
async def post_create_vrf(vrf: VrfBase):
    """
    Method responsible for creating a vrf
    """
    logger.info("Resource: Starting vrf creation: %s", vrf)

    create_vrf = await VrfFacade.create_vrf(vrf=vrf)
    if create_vrf["status"] == "success":
        logger.info("vrf was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_vrf["data"]) )

    logger.error("vrf was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_vrf["message"] )

@router.put("/vrf/{vrf_id}")
async def put_vrf(vrf_id: str, vrf: VrfBase):
    """
    Method responsible for update a vrf
    """
    logger.info("Resource: Starting vrf update: %s", vrf.dict())

    update_vrf = await VrfFacade.update_vrf(vrf_id=vrf_id, vrf=vrf)
    if update_vrf["status"] == "success":
        logger.info("vrf was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_vrf["data"]) )

    logger.error("vrf was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_vrf["message"] )

@router.get("/vrf")
async def get_vrfs():
    """
    Method responsible for listing all vrfs
    """
    logger.info("Resource: Starting vrfs get all")

    get_vrf = await VrfFacade.get_vrfs()
    if get_vrf["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_vrf["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_vrf["message"] )

@router.get("/vrf/{vrf_id}")
async def get_vrf(vrf_id: str):
    """
    Method responsible for listing a vrf
    """
    logger.info("Resource: Starting vrf get by id")

    get_vrf = await VrfFacade.get_vrf(vrf_id=vrf_id)
    if get_vrf["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_vrf["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_vrf["message"] )

@router.delete("/vrf/{vrf_id}")
async def delete_vrf(vrf_id: str):
    """
    Method responsible for delete a vrf
    """
    logger.info("Resource: Starting drop vrf id: %s", vrf_id)

    remove_vrf = await VrfFacade.delete_vrf(vrf_id=vrf_id)
    if remove_vrf["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_vrf["message"] )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_vrf["message"] )
