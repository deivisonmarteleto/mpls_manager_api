"""
Module responsible for path resrouce
"""

from time import sleep
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse



from src.app.core.ipam.paths.models import PathsBase
from src.app.ipam.paths.facade import PathFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger

logger = get_logger(__name__)


router = APIRouter(
    prefix="/ipam",
    tags=["path"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)

@router.post("/path")
async def post_create_path(path: PathsBase):
    """
    Method responsible for creating a path
    """
    logger.info("Resource: Starting path creation: %s", path)

    create_path = await PathFacade.create_path(path=path)
    if create_path["status"] == "success":
        logger.info("Path was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_path["data"]) )

    logger.error("Path was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_path["message"] )

@router.put("/path/{path_id}")
async def put_path(path_id: str, path: PathsBase):
    """
    Method responsible for update a path
    """
    logger.info("Resource: Starting path update: %s", path.dict())

    update_path = await PathFacade.update_path(path_id=path_id, path=path)
    if update_path["status"] == "success":
        logger.info("Path was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_path["data"]) )

    logger.error("Path was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_path["message"] )

@router.get("/path")
async def get_paths():
    """
    Method responsible for listing all paths
    """
    logger.info("Resource: Starting paths get all")

    get_path = await PathFacade.get_paths()
    if get_path["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_path["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_path["message"] )

@router.get("/path/device/{device_id}")
async def get_path_by_device(device_id: str):
    """
    Method responsible for get a path by device id
    """
    logger.info("Resource: Starting path get by device id")
    get_path = await PathFacade.get_path_by_device(device_id=device_id)
    if get_path["status"] == "success":
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_path["data"]) )

    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_path["message"] )

@router.delete("/path/{path_id}")
async def delete_path(path_id: str):
    """
    Method responsible for delete a path
    """
    logger.info("Resource: Starting path delete: %s", path_id)

    delete_path = await PathFacade.delete_path(path_id=path_id)
    if delete_path["status"] == "success":
        logger.info("Path was delete successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(delete_path["data"]) )

    logger.error("Path was not delete. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=delete_path["message"] )