"""
Module responsible for the l2domain facade
"""
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.core.ipam.l2domain.models import L2DomainBase
from src.app.core.ipam.l2domain.schema import L2DomainSchema
from src.app.ipam.vlans.facade import VlanFacade
from src.app.shared.messages import CREATE_SUCCESS, ALREADY_EXISTS, NOT_FOUND, UPDATE_SUCCESS, FOUND, DELETE_SUCCESS
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)

operation = "l2domain"


class L2DomainFacade:
    """
    Class responsible for the facade of the l2domain
    """

    @staticmethod
    async def create_l2domain(l2domain: L2DomainBase) -> CustomResponse:
        """
        Method responsible for creating l2domain
        """

        logger.info("Facade: Creating l2domain...")
        try:
            create_l2domain = await L2DomainSchema(**l2domain.model_dump(exclude_unset=True)).insert()

            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, create_l2domain.name), data=create_l2domain)

        except DuplicateKeyError as err:
            logger.error("Error creating l2domain (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, l2domain.name))

        except Exception as err:
            logger.error("Error creating l2domain (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [L2DomainFacade.create_l2domain]")

    @staticmethod
    async def update_l2domain(l2domain_id: str, l2domain: L2DomainBase) -> CustomResponse:
        """
        Method responsible for update a l2domain
        """

        logger.info("Facade: Update l2domain...")
        try:
            find_l2domain = await L2DomainSchema.get(l2domain_id, fetch_links=True)
            if find_l2domain is None:
                logger.error("l2domain %s not found! (update l2domain)", l2domain_id)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, l2domain_id))

            for field, value in l2domain.model_dump(exclude_unset=True).items():
                setattr(find_l2domain, field, value)

            await find_l2domain.replace()
            return CustomResponse.success(message=UPDATE_SUCCESS.format(operation, find_l2domain.name), data=find_l2domain)

        except DuplicateKeyError as err:
            logger.error("Error update l2domain (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, l2domain.name))

        except Exception as err:
            logger.error("Error update l2domain(Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [L2DomainFacade.update_l2domain]")

    @staticmethod
    async def get_l2domains() -> CustomResponse:
        """
        Method responsible for getting a l2domains
        """
        logger.info("Getting all l2domains")
        get_l2domain = await L2DomainSchema.find(fetch_links=True).to_list()
        if len(get_l2domain) == 0:
            logger.error("L2Domain %s not found! (get_l2domains)")
        else:
            logger.info("L2Domain found successfully . FIM (get_l2domains)! - %s", len(get_l2domain))

        return CustomResponse.success(message=FOUND.format(operation), data=get_l2domain)

    @staticmethod
    async def get_l2domains_by_id(l2domain_id: str) -> CustomResponse:
        """
        Method responsible for getting a l2domains
        """
        logger.info("Getting l2domains by id")
        get_l2domain = await L2DomainSchema.get(l2domain_id, fetch_links=True)
        if get_l2domain is None:
            logger.error("L2Domain %s not found! (get_l2domains)")
            return CustomResponse.failure(message=NOT_FOUND.format(operation, l2domain_id))

        logger.info("L2Domain found successfully . FIM (get_l2domains_by_id)! - %s", len(get_l2domain))
        return CustomResponse.success(message=FOUND.format(operation), data=get_l2domain)

    @staticmethod
    async def get_l2domains_by_location_id(location_id: str) -> CustomResponse:
        """
        Method responsible for getting a l2domains by location id
        """
        logger.info("Getting l2domains by location id...")
        get_l2domain = await L2DomainSchema.find(
            L2DomainSchema.location.id ==  ObjectId(location_id),fetch_links=True
        ).to_list()
        if len(get_l2domain) == 0:
            logger.error("L2Domain %s not found! (get_l2domains_by_location_id )", location_id)
            return CustomResponse.failure(message=NOT_FOUND.format(operation, location_id))

        logger.info("L2Domain found successfully . FIM! - %s", len(get_l2domain))
        return CustomResponse.success(message=FOUND.format(operation), data=get_l2domain)

    @staticmethod
    async def delete_l2domain(l2domain_id: str) -> CustomResponse:
        """
        Method responsible for deleting a l2domain
        """
        logger.info("Facade: Deleting l2domain_id...")

        delete_l2domain = L2DomainSchema.find(L2DomainSchema.id  == ObjectId(l2domain_id), fetch_links=True)
        if delete_l2domain is None:
            logger.error("L2Domain %s not found! (delete_l2domain)", l2domain_id)
            return CustomResponse.failure(message=NOT_FOUND.format(operation, l2domain_id))

        logger.info("Facade: Checking if L2Domain has associated Vlans: %s", l2domain_id)

        await VlanFacade.delete_vlan_by_l2domain_id(l2domain_id=l2domain_id)

        await delete_l2domain.delete()
        logger.info("Facade: Deleting L2Domain: %s", l2domain_id)
        return CustomResponse.success(message=DELETE_SUCCESS.format(operation, l2domain_id), data=l2domain_id)
