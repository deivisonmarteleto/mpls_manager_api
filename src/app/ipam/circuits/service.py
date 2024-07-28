"""
module for circuits service
"""

from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError



from src.app.core.ipam.circuits.models import CircuitsBase
from src.app.core.ipam.circuits.schema import CircuitsSchema
from src.app.core.ipam.interfaces.lag.schema import InterfaceLagSchema
from src.app.core.ipam.interfaces.single.schema import InterfaceSingleSchema
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)

openation = "interface circuit"

INTERFACE_LINKED: str = "To create a new circuit it is necessary to have interfaces or lag linked."

class CircuitsService:
    """
    Class responsible for the service of the circuit
    """

    @staticmethod
    async def validate_interface_circuit(circuit: CircuitsBase) -> CustomResponse:
        """
        Method responsible for validating circuit
        """
        logger.info("Service: Validating circuit...")
        if (circuit.interface_dst is None and circuit.lag_dst is None) or (circuit.interface_src is None and circuit.lag_src is None):
            return CustomResponse.failure(message=INTERFACE_LINKED)

        if (circuit.interface_dst is not None and circuit.lag_dst is not None) or (circuit.interface_src is not None and circuit.lag_src is not None):
            return CustomResponse.failure(message=INTERFACE_LINKED)

        logger.info("Service: Validating circuit, step 1: ok.")

        if circuit.interface_src:
            logger.info("Service: Validating circuit, select interface from...")
            find_interface_src = await InterfaceSingleSchema.get(circuit.interface_src, fetch_links=True)
            if find_interface_src is None:
                return CustomResponse.failure(message=NOT_FOUND.format(openation, circuit.interface_src))

            device_id_from = str(find_interface_src.device.id)
        elif circuit.lag_src:
            logger.info("Service: Validating circuit, select lag from...")
            find_interface_src = await InterfaceLagSchema.get(circuit.lag_src, fetch_links=True)
            if find_interface_src is None:
                return CustomResponse.failure(message=NOT_FOUND.format(openation, circuit.lag_src))

            device_id_from = str(find_interface_src.device.id)

        logger.info("Service: Validating circuit, step 2: ok.")

        if circuit.interface_dst:
            logger.info("Service: Validating circuit, select interface to...")
            find_interface_dst = await InterfaceSingleSchema.get(circuit.interface_dst, fetch_links=True)
            if find_interface_dst is None:
                return CustomResponse.failure(message=NOT_FOUND.format(openation, circuit.interface_dst))

            device_id_to = str(find_interface_dst.device.id)

        elif circuit.lag_dst:
            logger.info("Service: Validating circuit, select lag to...")
            find_interface_dst = await InterfaceLagSchema.get(circuit.lag_dst, fetch_links=True)
            if find_interface_dst is None:
                return CustomResponse.failure(message=NOT_FOUND.format(openation, circuit.lag_dst))

            device_id_to = str(find_interface_dst.device.id)

        logger.info("Service: Validating circuit, step 3: ok.")

        if device_id_from == device_id_to:
            return CustomResponse.failure(message="It is not possible to create circuits on the same equipment.")


        return CustomResponse.success(message="Circuit validated successfully")
