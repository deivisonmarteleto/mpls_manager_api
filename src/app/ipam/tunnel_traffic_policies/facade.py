"""
Module responsible for facade tunnel traffic policies
"""


from datetime import datetime
from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import  DeleteRules

from src.app.core.ipam.tunnel_traffic_policies.models import TunnelTrafficPoliciesBase
from src.app.core.ipam.tunnel_traffic_policies.schema import TunnelTrafficPoliciesSchema
from src.app.shared.messages import (ALREADY_EXISTS, CREATE_SUCCESS,
                                     DELETE_SUCCESS, FOUND, NOT_FOUND,
                                     UPDATE_SUCCESS)
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)


operation = "tunnel traffic policies"



class TunnelTrafficPoliciesFacade:
    """
    Class responsible for the facade of the tunnel traffic policies
    """

    @staticmethod
    async def get_tunnel_traffic_policies() -> CustomResponse:
        """
        Method responsible for get all tunnel traffic policies
        """

        logger.info("Facade: Get all tunnel traffic policies...")
        try:

            find_tunnel_traffic_policies = await TunnelTrafficPoliciesSchema.find(fetch_links=True).to_list()

            logger.info("Facade: Get all tunnel traffic policies success: %s", find_tunnel_traffic_policies)
            return CustomResponse.success(message=FOUND.format(operation), data=find_tunnel_traffic_policies)

        except Exception as err:
            logger.error("Error get all tunnel traffic policies (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelTrafficPoliciesFacade.get_tunnel_traffic_policies]")

    @staticmethod
    async def update_tunnel_traffic_policies(tunnel_traffic_policies: Type[TunnelTrafficPoliciesBase], tunnel_traffic_policies_id: str) -> CustomResponse:
        """
        Method responsible for update tunnel traffic policies
        """

        logger.info("Facade: Updating tunnel traffic policies...")
        try:
            find_tunnel_traffic_policies = await TunnelTrafficPoliciesSchema.get(ObjectId(tunnel_traffic_policies_id))
            if find_tunnel_traffic_policies is None:
                logger.error("Tunnel traffic policies %s not found!", tunnel_traffic_policies_id)
                return CustomResponse.failure(message=NOT_FOUND.format("tunnel traffic policies", tunnel_traffic_policies_id))

            for field, value in tunnel_traffic_policies.model_dump(exclude_unset=True).items():
                if field in  ["id", "_id"]:
                    continue
                current_value = getattr(find_tunnel_traffic_policies, field)

                if value != current_value or (value is None and current_value is not None):
                    logger.info("Facade: Update find_tunnel_traffic_policies field: %s", field)
                    setattr(find_tunnel_traffic_policies, field, value)

            await find_tunnel_traffic_policies.save()
            logger.info("Facade: Updating tunnel traffic policies success")
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, tunnel_traffic_policies.name), data=find_tunnel_traffic_policies)

        except Exception as err:
            logger.error("Error updating tunnel traffic policies (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelTrafficPoliciesFacade.update_tunnel_traffic_policies]")

    @staticmethod
    async def create_tunnel_traffic_policies(tunnel_traffic_policies: Type[TunnelTrafficPoliciesBase]) -> CustomResponse:
        """
        Method responsible for create tunnel traffic policies
        """

        logger.info("Facade: Creating tunnel traffic policies...")
        try:
            tunnel_traffic_policies.created_at = datetime.now()
            create_tunnel_traffic_policies =  TunnelTrafficPoliciesSchema(**tunnel_traffic_policies.model_dump(exclude_unset=True))
            await create_tunnel_traffic_policies.insert()

            logger.info("Facade: Creating tunnel traffic policies success: %s", create_tunnel_traffic_policies.dict())
            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, tunnel_traffic_policies.name), data=create_tunnel_traffic_policies)

        except DuplicateKeyError as err:
            logger.error("Error creating tunnel traffic policies (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, tunnel_traffic_policies.name))

        except Exception as err:
            logger.error("Error creating tunnel traffic policies (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelTrafficPoliciesFacade.create_tunnel_traffic_policies]")

    @staticmethod
    async def delete_tunnel_traffic_policies(tunnel_traffic_policies_id: str) -> CustomResponse:
        """
        Method responsible for delete a tunnel traffic policies
        """

        logger.info("Facade: Delete tunnel traffic policies...")
        try:
            find_tunnel_traffic_policies = await TunnelTrafficPoliciesSchema.get(ObjectId(tunnel_traffic_policies_id))
            if find_tunnel_traffic_policies is None:
                logger.error("Tunnel traffic policies %s not found!", tunnel_traffic_policies_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, tunnel_traffic_policies_id))

            await find_tunnel_traffic_policies.delete()
            logger.info("Facade: Delete tunnel traffic policies success...")
            return CustomResponse.success(message=DELETE_SUCCESS.format(operation, find_tunnel_traffic_policies.name))

        except Exception as err:
            logger.error("Error delete tunnel traffic policies (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [TunnelTrafficPoliciesFacade.delete_tunnel_traffic_policies]")
