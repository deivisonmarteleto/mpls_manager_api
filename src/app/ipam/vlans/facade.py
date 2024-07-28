"""
Module responsible for the vlans facade
"""
from beanie.operators import In, Set
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.core.ipam.l2domain.schema import L2DomainSchema
from src.app.core.ipam.vlans.models import VlanBase
from src.app.core.ipam.vlans.schema import VlanSchema
from src.app.shared.messages import ALREADY_EXISTS, CREATE_SUCCESS, NOT_FOUND, FOUND, DELETE_SUCCESS
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)

operation = "vlan"

class VlanFacade:
    """
    Class responsible for the facade of the vlans
    """

    @staticmethod
    async def create_vlan(vlan: VlanBase) -> CustomResponse:
        """
        Method responsible for creating vlan
        """

        logger.info("Facade: Creating vlan...")
        try:
            l2domain = await L2DomainSchema.get(vlan.l2domain)
            if l2domain is None:
                return CustomResponse.failure(message="L2Domain %s não encontrado! (Vlan)" % vlan.l2domain)

            logger.info("Facade: Success find l2domain: %s", l2domain)

            if vlan.unique is False:
                logger.info("Facade: Select not unique vlan...")
                check_vlan = await VlanSchema.find(
                    VlanSchema.l2domain.id == l2domain.id,
                    VlanSchema.number == vlan.number
                ).to_list()

            else:
                logger.info("Facade: Checking if vlan is unique...")
                check_vlan = await VlanSchema.find(
                    {'number' :vlan.number},fetch_links=True
                ).to_list()

            if len(check_vlan) > 0:
                logger.error("Vlan %s already exists! (create_vlan)", vlan.number)
                return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, vlan.number))

            create_vlan = await VlanSchema(**vlan.model_dump(exclude_unset=True)).insert()
            return CustomResponse.success(message=CREATE_SUCCESS.format(operation, create_vlan.name), data=create_vlan.name)

        except DuplicateKeyError as err:
            logger.error("Error creating vlan (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, create_vlan.name))

        except Exception as err:
            logger.error("Error creating vlan (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VlanFacade.create_vlan]")

    @staticmethod
    async def create_vlan_range(vlan_start: int, vlan_end: int, l2domain_id: str) -> CustomResponse:
        """
        Method responsible for creating vlan range
        """

        logger.info("Facade: Creating vlan range...")
        try:
            if vlan_start >= vlan_end:
                logger.error("Vlan start %s is greater than vlan end %s", vlan_start, vlan_end)
                return CustomResponse.failure(message="Range de vlan não está configurado corretamente.")

            if vlan_start < 2 or vlan_end > 4094:
                logger.error("Vlan range %s-%s is out of range", vlan_start, vlan_end)
                return CustomResponse.failure(message="Range de vlan está configurado fora do limite permitido.")

            find_l2domain = await L2DomainSchema.get(l2domain_id)
            if find_l2domain is None:
                return CustomResponse.failure(message=NOT_FOUND.format(operation, l2domain_id))

            vlan_range = range(vlan_start, vlan_end)

            find_vlans = await VlanSchema.find(
                VlanSchema.l2domain.id == ObjectId(l2domain_id),
                In(VlanSchema.number, list(vlan_range))
            ).to_list()
            if len(find_vlans) > 0:
                logger.error("Vlan range already exists! (create_vlan_range)")
                return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, f"{vlan_start}-{vlan_end}"))

            vlan_range_list = [
                VlanSchema(
                    name=f"{find_l2domain.name}-VLAN{vlan}", number=vlan,  description="Criado automaticamente", l2domain=l2domain_id
                ) for vlan in vlan_range

            ]
            await VlanSchema.insert_many(vlan_range_list)

            return CustomResponse.success(message="Range de Vlans %s foi criados com sucesso!" % f"{vlan_start}-{vlan_end}")

        except DuplicateKeyError as err:
            logger.error("Error creating vlan range (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation,  f"{vlan_start}-{vlan_end}"))

        except Exception as err:
            logger.error("Error creating vlan range (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VlanFacade.create_vlan_range]")

    @staticmethod
    async def update_vlan(vlan_id: str, vlan: VlanBase) -> CustomResponse:
        """
        Method responsible for update a vlan
        """

        logger.info("Facade: Update vlan...")
        try:
            find_vlan = await VlanSchema.get(vlan_id, fetch_links=True)
            if find_vlan is None:
                logger.error("Vlan %s not found! (update_vlan)", find_vlan)
                return CustomResponse.failure(message=NOT_FOUND.format(operation, find_vlan))

            for field, value in vlan.model_dump(exclude_unset=True).items():
                if field == "l2domain":
                    continue
                setattr(find_vlan, field, value)

            await find_vlan.replace()
            return CustomResponse.success(message="Vlan %s foi atualizado com sucesso!" % find_vlan.name, data=find_vlan.id)

        except DuplicateKeyError as err:
            logger.error("Error update vlan (DuplicateKeyError): %s", err)
            return CustomResponse.failure(message=ALREADY_EXISTS.format(operation, find_vlan.name))

        except Exception as err:
            logger.error("Error update vlan (Exception): %s", err)
            return CustomResponse.failure(message="Interno error: [VlanFacade.update_vlan]")

    @staticmethod
    async def get_vlans_by_l2domain_id(l2domain_id: str) -> CustomResponse:
        """
        Method responsible for getting a vlans by l2domain id
        """
        logger.info("Getting all vlans by l2domain id...")
        get_vlans = await VlanSchema.find(
            VlanSchema.l2domain.id == ObjectId(l2domain_id),
            fetch_links=True,
            nesting_depth=2,
        ).to_list()
        if len(get_vlans) == 0:
            logger.error("Vlans by l2domain %s not found!", l2domain_id)
            return CustomResponse.failure(message=NOT_FOUND.format(operation, l2domain_id))

        logger.info("Vlans by l2domain found successfully . FIM! - %s", len(get_vlans))
        return CustomResponse.success(message=FOUND.format(l2domain_id), data=get_vlans)

    @staticmethod
    async def delete_vlan(vlan_id: str) -> CustomResponse:
        """
        Method responsible for deleting a vlan
        """
        logger.info("Facade: Deleting vlan: %s", vlan_id)

        delete_vlan = await VlanSchema.get(vlan_id)
        if delete_vlan is None:
            logger.error("Vlan %s not found! (delete_vlan)", vlan_id)
            return CustomResponse.failure(message=NOT_FOUND.format(operation, vlan_id))

        logger.info("Facade: Deleting vlan: %s", delete_vlan.id)
        await delete_vlan.delete()
        return CustomResponse.success(message=FOUND.format(operation, delete_vlan.name), data=delete_vlan.id)

    @staticmethod
    async def delete_vlan_range(vlan_start: int, vlan_end: int, l2domain_id: str) -> CustomResponse:
        """
        Method responsible for deleting a vlan
        """
        logger.info("Facade: Deleting vlan range: %s", l2domain_id)
        if vlan_start >= vlan_end:
            logger.error("Vlan start %s is greater than vlan end %s (delete ranger)", vlan_start, vlan_end)
            return CustomResponse.failure(message="Range de vlan está configurado corretamente. Não foi possível deletar range de vlan.")

        vlan_range = range(vlan_start, vlan_end)

        find_vlans = VlanSchema.find(
            VlanSchema.l2domain.id == ObjectId(l2domain_id),
            In(VlanSchema.number, list(vlan_range))
        )
        if find_vlans is None:
            logger.error("Vlan range not exists! (delete_vlan_range)")
            return CustomResponse.failure(message=NOT_FOUND.format(operation, f"{vlan_start}-{vlan_end}"))

        await find_vlans.delete()
        return CustomResponse.success(message=FOUND.format(f"{vlan_start}-{vlan_end}"), data=f"{vlan_start}-{vlan_end}")

    @staticmethod
    async def delete_vlan_by_l2domain_id(l2domain_id: str) -> CustomResponse:
        """
        Method responsible for deleting a vlan by l2domain id
        """
        logger.info("Facade: Deleting vlan by l2domain: %s", l2domain_id)

        find_vlans = await  VlanSchema.find(
            VlanSchema.l2domain.id == ObjectId(l2domain_id)
        ).to_list()

        if len(find_vlans) == 0:
            logger.error("Vlan l2 domain not exists! (delete_vlan_range)")
            return CustomResponse.failure(message=NOT_FOUND.format(operation, l2domain_id))

        for vlan in find_vlans:
            logger.info("Facade: Deleting vlan: %s", vlan.id)
            await vlan.delete()

        logger.info("Facade: Deleting vlan by l2domain success: %s", l2domain_id)
        return CustomResponse.success(message=DELETE_SUCCESS.format(operation, l2domain_id))
