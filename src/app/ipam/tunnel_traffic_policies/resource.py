"""
Module responsible for tunnel traffic policies schema
"""

from time import sleep
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse



from src.app.core.ipam.tunnel_traffic_policies.models import TunnelTrafficPoliciesBase
from src.app.ipam.tunnel_traffic_policies.facade import TunnelTrafficPoliciesFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)


router = APIRouter(
    prefix="/ipam",
    tags=["tunnel traffic policies"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)


@router.get("/tunnel_traffic_policies")
async def get_tunnel_traffic_policies():
    """
    Method responsible for listing all tunnel traffic policies
    """
    logger.info("Resource: Starting tunnel traffic policies get all")

    get_tunnel_traffic_policies = await TunnelTrafficPoliciesFacade.get_tunnel_traffic_policies()
    if get_tunnel_traffic_policies["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_tunnel_traffic_policies["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_tunnel_traffic_policies["message"] )

@router.post("/tunnel_traffic_policies")
async def post_create_tunnel_traffic_policies(tunnel_traffic_policies: TunnelTrafficPoliciesBase):
    """
    Method responsible for creating a tunnel traffic policies
    """
    logger.info("Resource: Starting tunnel traffic policies creation: %s", tunnel_traffic_policies)

    create_tunnel_traffic_policies = await TunnelTrafficPoliciesFacade.create_tunnel_traffic_policies(tunnel_traffic_policies=tunnel_traffic_policies)
    if create_tunnel_traffic_policies["status"] == "success":
        logger.info("tunnel traffic policies was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_tunnel_traffic_policies["data"]) )

    logger.error("tunnel traffic policies was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_tunnel_traffic_policies["message"] )

@router.put("/tunnel_traffic_policies/{tunnel_traffic_policies_id}")
async def put_tunnel_traffic_policies(tunnel_traffic_policies_id: str, tunnel_traffic_policies: TunnelTrafficPoliciesBase):
    """
    Method responsible for update a tunnel traffic policies
    """
    logger.info("Resource: Starting tunnel traffic policies update: %s", tunnel_traffic_policies.dict())

    update_tunnel_traffic_policies = await TunnelTrafficPoliciesFacade.update_tunnel_traffic_policies(tunnel_traffic_policies_id=tunnel_traffic_policies_id, tunnel_traffic_policies=tunnel_traffic_policies)
    if update_tunnel_traffic_policies["status"] == "success":
        logger.info("tunnel traffic policies was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_tunnel_traffic_policies["data"]) )

    logger.error("tunnel traffic policies was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_tunnel_traffic_policies["message"] )

@router.delete("/tunnel_traffic_policies/{tunnel_traffic_policies_id}")
async def delete_tunnel_traffic_policies(tunnel_traffic_policies_id: str):
    """
    Method responsible for delete a tunnel traffic policies
    """
    logger.info("Resource: Starting tunnel traffic policies delete: %s", tunnel_traffic_policies_id)

    delete_tunnel_traffic_policies = await TunnelTrafficPoliciesFacade.delete_tunnel_traffic_policies(tunnel_traffic_policies_id=tunnel_traffic_policies_id)
    if delete_tunnel_traffic_policies["status"] == "success":
        logger.info("tunnel traffic policies was delete successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(delete_tunnel_traffic_policies["data"]) )

    logger.error("tunnel traffic policies was not delete. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=delete_tunnel_traffic_policies["message"] )