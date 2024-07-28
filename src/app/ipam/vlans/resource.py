"""
Module responsible for vlans routes
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse


from src.app.core.ipam.vlans.models import VlanBase
from src.app.ipam.vlans.facade import VlanFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ipam",
    tags=["vlans"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/vlan")
async def post_create_vlan(vlan: VlanBase):
    """
    Method responsible for creating a vlan
    """
    logger.info("Resource: Starting vlan creation: %s", vlan)

    create_vlan = await VlanFacade.create_vlan(vlan=vlan)
    if create_vlan["status"] == "success":
        logger.info("vlan was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_vlan["data"]) )

    logger.error("vlan was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_vlan["message"] )

@router.post("/vlan/range/{l2domain_id}/{vlan_start}/{vlan_end}")
async def post_create_vlan_range(l2domain_id: str, vlan_start: int, vlan_end: int):
    """
    Method responsible for creating a vlan range
    """
    logger.info("Resource: Starting vlan range creation: %s", l2domain_id)

    create_vlan = await VlanFacade.create_vlan_range(vlan_start=vlan_start, vlan_end=vlan_end, l2domain_id=l2domain_id)
    if create_vlan["status"] == "success":
        logger.info("vlan range was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_vlan["data"]) )

    logger.error("vlan range was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_vlan["message"] )

@router.put("/vlan/{vlan_id}")
async def put_vlan(vlan_id: str, vlan: VlanBase):
    """
    Method responsible for update a vlan
    """
    logger.info("Resource: Starting vlan update: %s", vlan.dict())

    update_vlan = await VlanFacade.update_vlan(vlan_id=vlan_id, vlan=vlan)
    if update_vlan["status"] == "success":
        logger.info("Vlan was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_vlan["data"]) )

    logger.error("Vlan was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_vlan["message"] )

@router.get("/vlan/{l2domain_id}")
async def get_vlans_by_l2domain(l2domain_id: str):
    """
    Method responsible for listing all vlan
    """
    logger.info("Resource: Starting vlan get all")

    get_vlans = await VlanFacade.get_vlans_by_l2domain_id(l2domain_id=l2domain_id)

    if get_vlans["status"] == "success":
        logger.info("vlan get all successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_vlans["data"]))

    logger.error("vlan get all error. FIM!")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=get_vlans["message"])

@router.delete("/vlan/{vlan_id}")
async def delete_vlan(vlan_id: str):
    """
    Method responsible for delete vlan
    """
    logger.info("Resource: Starting drop vlan id: %s", vlan_id)

    remove_vlan = await VlanFacade.delete_vlan(vlan_id=vlan_id)
    if remove_vlan["status"] == "success":
        logger.info("vlan was removed successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_vlan["message"] )

    logger.error("vlan was not removed. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_vlan["message"] )

@router.delete("/vlan/range/{l2domain_id}/{vlan_start}/{vlan_end}")
async def delete_vlan_range(l2domain_id: str, vlan_start: int, vlan_end: int):
    """
    Method responsible for delete vlan range
    """
    logger.info("Resource: Starting drop vlan range id: %s", l2domain_id)

    remove_vlan = await VlanFacade.delete_vlan_range(l2domain_id=l2domain_id, vlan_start=vlan_start, vlan_end=vlan_end)
    if remove_vlan["status"] == "success":
        logger.info("vlan range was removed successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_vlan["message"] )

    logger.error("vlan range was not removed. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_vlan["message"] )
