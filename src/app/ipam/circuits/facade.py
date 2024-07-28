"""
Module responsible for circuits Facade
"""

from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError



from src.app.core.ipam.circuits.models import CircuitsBase
from src.app.core.ipam.circuits.schema import CircuitsSchema
from src.app.ipam.circuits.service import CircuitsService
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)

operation_error = "circuit id or name"
operation = "circuit"

class CircuitsFacade:
    """
    Class responsible for the facade of the circuit
    """

    @staticmethod
    async def create_circuit(circuit: Type[CircuitsBase]) -> CustomResponse:
        """
        Method responsible for creating circuit
        """

        logger.info("Facade: Creating circuit...")
        try:

            # validate_circuit = await CircuitsService.validate_interface_circuit(circuit=circuit)
            # if validate_circuit["status"] == "failure":
            #     return validate_circuit

            circuit.created_at = datetime.now().isoformat()
            create_circuit =  CircuitsSchema(**circuit.model_dump(exclude_unset=True))
            logger.info("Facade: Creating circuit: %s", create_circuit)
            await create_circuit.insert()

            logger.info("Facade: Creating circuit success: %s", create_circuit.dict())

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, circuit.name), data=create_circuit)

        except DuplicateKeyError as err:
            logger.error("Error creating circuit (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation_error, circuit.name))

        except Exception as err:
            logger.error("Error creating circuit (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [CircuitFacade.create_circuit]")

    @staticmethod
    async def update_circuit(circuit_id: str, circuit: Type[CircuitsBase]) -> CustomResponse:
        """
        Method responsible for update a circuit
        """

        logger.info("Facade: Update circuit...")
        try:
            find_circuit = await CircuitsSchema.get(circuit_id, fetch_links=True)
            if find_circuit is None:
                logger.error("Facade: Update Circuit %s not found!", circuit_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, circuit_id))

            logger.info("Facade: find circuit success [update]: %s", find_circuit.dict())

            for field, value in find_circuit.model_dump(exclude_unset=True).items():
                setattr(find_circuit, field, value)
                update_circuit = await find_circuit.replace()

            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, circuit.name), data=update_circuit)

        except DuplicateKeyError as err:
            logger.error("Error update Circuit (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, circuit.name))

        except Exception as err:
            logger.error("Error update Circuit (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [CircuitFacade.update_circuit]")

    @staticmethod
    async def get_circuits() -> CustomResponse:
        """
        Method responsible for get all circuits
        """

        logger.info("Facade: Get all circuits...")
        try:
            circuits = await CircuitsSchema.find(fetch_links=True).to_list()
            return CustomResponse.success(message=FOUND.format(operation), data=circuits)

        except Exception as err:
            logger.error("Error get all circuits (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [CircuitFacade.get_circuits]")

    @staticmethod
    async def get_circuit(circuit_id: str) -> CustomResponse:
        """
        Method responsible for get a circuit
        """

        logger.info("Facade: Get circuit...")
        try:
            circuit = await CircuitsSchema.get(circuit_id, fetch_links=True)
            if circuit is None:
                logger.error("Circuit %s not found!", circuit_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, circuit_id))

            return CustomResponse.success(message=FOUND.format(operation), data=circuit)

        except Exception as err:
            logger.error("Error get circuit (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [CircuitFacade.get_circuit]")

    @staticmethod
    async def delete_circuit(circuit_id: str) -> CustomResponse:
        """
        Method responsible for delete a circuit
        """

        logger.info("Facade: Deleting circuit: %s", circuit_id)
        try:
            delete_circuit = await CircuitsSchema.get(circuit_id)
            if delete_circuit is None:
                logger.error("Circuit %s not found! (delete_circuit)", circuit_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, circuit_id))

            await delete_circuit.delete()
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, delete_circuit.name), data=delete_circuit.name)

        except Exception as err:
            logger.error("Error delete circuit (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [CircuitFacade.delete_circuit]")
