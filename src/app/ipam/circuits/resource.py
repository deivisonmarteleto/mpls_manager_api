"""
Module responsible for circuits Resource
"""


from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.app.core.ipam.circuits.models import CircuitsBase
from src.app.ipam.circuits.facade import CircuitsFacade
from src.app.shared.serialize import SerializationFilter
# from src.dependencies import authorization
from src.logging import get_logger


logger = get_logger(__name__)


router = APIRouter(
    prefix="/ipam",
    tags=["circuits"],
    #dependencies=[Depends(authorization, use_cache=True)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "unauthorized"}},
)


@router.post("/circuits")
async def post_create_circuit(circuit: CircuitsBase):
    """
    Method responsible for creating a circuit
    """
    logger.info("Resource: Starting circuit creation: %s", circuit)

    create_circuit = await CircuitsFacade.create_circuit(circuit=circuit)
    if create_circuit["status"] == "success":
        logger.info("circuit was created successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(create_circuit["data"]) )

    logger.error("circuit was not created. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=create_circuit["message"] )


@router.put("/circuits/{circuit_id}")
async def put_circuit(circuit_id: str, circuit: CircuitsBase):
    """
    Method responsible for update a circuit
    """
    logger.info("Resource: Starting circuit update: %s", circuit.dict())

    update_circuit = await CircuitsFacade.update_circuit(circuit_id=circuit_id, circuit=circuit)
    if update_circuit["status"] == "success":
        logger.info("Circuit was update successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SerializationFilter.response(update_circuit["data"]) )

    logger.error("Circuit was not update. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=update_circuit["message"] )


@router.get("/circuits")
async def get_circuits():
    """
    Method responsible for listing all circuits
    """
    logger.info("Resource: Starting circuits get all")

    get_circuit = await CircuitsFacade.get_circuits()
    if get_circuit["status"] == "success":
        logger.info("Circuits were listed successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_circuit["data"]) )

    logger.error("Circuits were not listed. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_circuit["message"] )


@router.get("/circuits/{circuit_id}")
async def get_circuit(circuit_id: str):
    """
    Method responsible for get a circuit by id
    """
    logger.info("Resource: Starting circuit get by id")

    get_circuit = await CircuitsFacade.get_circuit(circuit_id=circuit_id)
    if get_circuit["status"] == "success":
        logger.info("Circuit was found successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=SerializationFilter.response(get_circuit["data"]) )

    logger.error("Circuit was not found. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=get_circuit["message"] )


@router.delete("/circuits/{circuit_id}")
async def delete_circuit(circuit_id: str):
    """
    Method responsible for delete a circuit
    """
    logger.info("Resource: Starting circuit delete by id")

    remove_circuit = await CircuitsFacade.delete_circuit(circuit_id=circuit_id)
    if remove_circuit["status"] == "success":
        logger.info("Circuit was deleted successfully. FIM!")
        return JSONResponse(status_code=status.HTTP_200_OK, content=remove_circuit["data"])

    logger.error("Circuit was not deleted. FIM!")
    return JSONResponse(status_code=status.HTTP_302_FOUND, content=remove_circuit["message"] )
