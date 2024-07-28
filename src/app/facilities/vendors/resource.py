"""
Module responsible for vendor routes
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.facilities.vendors.models import VendorBase
from src.app.facilities.vendors.facade import VendorFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/facilities",
    tags=["vendor"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/vendor")
async def post_create_vendor(vendor: VendorBase):
    """
    Method responsible for creating a vendor
    """
    logger.info("Resource: Starting vendor creation: %s", VendorBase)

    create_vendor = await VendorFacade.create_vendor(vendor=vendor)
    if create_vendor["status"] == "success":
        logger.info("Vendor was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_vendor["data"]) )

    logger.error("Vendor was not created. FIM! - %s" ,create_vendor["message"])
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_vendor["message"] )

@router.put("/vendor/{vendor_id}")
async def put_vendor(vendor_id: str, vendor: VendorBase):
    """
    Method responsible for update a vendor
    """
    logger.info("Resource: Starting vendor update: %s", vendor)

    update_vendor = await VendorFacade.update_vendor(vendor_id=vendor_id, vendor=vendor)
    if update_vendor["status"] == "success":
        logger.info("Vendor was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_vendor["data"]) )

    logger.error("Vendor was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_vendor["message"] )

@router.get("/vendor")
async def get_vendors():
    """
    Method responsible for listing all vendors
    """
    logger.info("Resource: Starting vendors get all")

    get_vendor = await VendorFacade.get_vendors()
    if get_vendor["status"] == "success":
        logger.info("Vendors get all successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_vendor["data"]))

    logger.error("Vendors get all error. FIM!")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=get_vendor["message"])

@router.delete("/vendor/{vendor_id}", response_model=str)
async def delete_vendor(vendor_id: str):
    """
    Method responsible for delete avendor
    """
    logger.info("Resource: Starting drop vendor id: %s", vendor_id)

    remove_vendor = await VendorFacade.delete_vendor(vendor_id=vendor_id)
    if remove_vendor["status"] == "success":
        logger.info("Vendor was deleted successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_vendor["message"] )

    logger.error("Vendor was not deleted. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_vendor["message"] )
