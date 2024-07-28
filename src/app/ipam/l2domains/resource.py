"""
Module responsible for l2 domain routes
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.ipam.l2domain.models import L2DomainBase
from src.app.ipam.l2domains.facade import L2DomainFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ipam",
    tags=["l2domains"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/l2domain")
async def post_create_l2domain(l2domain: L2DomainBase):
    """
    Method responsible for creating a l2domain
    """
    logger.info("Resource: Starting l2domain creation: %s", l2domain)

    create_l2domain = await L2DomainFacade.create_l2domain(l2domain=l2domain)
    if create_l2domain["status"] == "success":
        logger.info("l2domain was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_l2domain["data"]) )

    logger.error("l2domain was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_l2domain["message"] )

@router.put("/l2domain/{l2domain_id}")
async def put_l2domain(l2domain_id: str, l2domain: L2DomainBase):
    """
    Method responsible for update a l2domain
    """
    logger.info("Resource: Starting l2domain update: %s", l2domain.dict())

    update_l2domain = await L2DomainFacade.update_l2domain(l2domain_id=l2domain_id, l2domain=l2domain)
    if update_l2domain["status"] == "success":
        logger.info("L2 Domain was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_l2domain["data"]) )

    logger.error("L2 Domain was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_l2domain["message"] )

@router.get("/l2domain")
async def get_l2domains():
    """
    Method responsible for listing all l2domains
    """
    logger.info("Resource: Starting l2domains get all")

    get_l2domain = await L2DomainFacade.get_l2domains()

    if get_l2domain["status"] == "success":
        logger.info("L2domain get all successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_l2domain["data"]))

    logger.error("L2Domain get all error. FIM!")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=get_l2domain["message"])

@router.delete("/l2domain/{l2domain_id}")
async def delete_l2domain(l2domain_id: str):
    """
    Method responsible for delete l2domain
    """
    logger.info("Resource: Starting drop l2domain id: %s", l2domain_id)

    remove_l2domain = await L2DomainFacade.delete_l2domain(l2domain_id=l2domain_id)
    if remove_l2domain["status"] == "success":
        logger.info("L2 Domain was deleted successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_l2domain["message"] )

    logger.error("L2 Domain was not deleted. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_l2domain["message"] )
