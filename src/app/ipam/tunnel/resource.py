"""
module for tunnel resource
"""
from time import sleep
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse


from src.app.core.ipam.tunnel.models import TunnelBase
from src.app.ipam.tunnel.facade import TunnelFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ipam",
    tags=["tunnel"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)


@router.post("/tunnel")
async def post_create_tunnel(tunnel: TunnelBase):
    """
    Method responsible for creating a tunnel
    """
    logger.info("Resource: Starting tunnel creation: %s", tunnel)

    create_tunnel = await TunnelFacade.create_tunnel(tunnel=tunnel)
    if create_tunnel["status"] == "success":
        logger.info("tunnel was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_tunnel["data"]) )

    logger.error("tunnel was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_tunnel["message"] )

@router.put("/tunnel/{tunnel_id}")
async def put_tunnel(tunnel_id: str, tunnel: TunnelBase):
    """
    Method responsible for update a tunnel
    """
    logger.info("Resource: Starting tunnel update: %s", tunnel.dict())

    update_tunnel = await TunnelFacade.update_tunnel(tunnel_id=tunnel_id, tunnel=tunnel)
    if update_tunnel["status"] == "success":
        logger.info("tunnel was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_tunnel["data"]) )

    logger.error("tunnel was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_tunnel["message"] )

@router.get("/tunnel")
async def get_tunnel_by_device():
    """
    Method responsible for listing all tunnel by device id
    """
    logger.info("Resource: Starting tunnel get by device id")
    get_tunnel = await TunnelFacade.get_tunnel()
    if get_tunnel["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_tunnel["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_tunnel["message"] )

@router.delete("/tunnel/{tunnel_id}")
async def delete_tunnel(tunnel_id: str):
    """
    Method responsible for delete a tunnel
    """
    logger.info("Resource: Starting tunnel delete")
    delete_tunnel = await TunnelFacade.delete_tunnel(tunnel_id=tunnel_id)
    if delete_tunnel["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(delete_tunnel["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=delete_tunnel["message"] )
