"""
Module responsible for shared validade functions
"""


from src.app.core.ipam.devices.schema import DevicesSchema

from src.app.shared.messages import ALREADY_EXISTS, FOUND, NOT_FOUND, UPDATE_SUCCESS, CREATE_SUCCESS, DELETE_SUCCESS
from src.app.shared.response import CustomResponse
from src.logging import get_logger

logger = get_logger(__name__)



operation_ip = "Ip Address"

# class Validate:
#     """
#     Class responsible for the validate
#     """

#     @staticmethod
#     async def validate_device_ipaddr(ipaddr: str) -> bool:
#         """
#         Method responsible for validate device ipaddr
#         """

#         logger.info("Validate: Validate device ipaddr...")
#         try:
#             check_ipaddr = await DevicesSchema.find().to_list()
#             for ip in check_ipaddr:
#                 if device == ip.ipaddr:
#                     return False

#             logger.info("Validate: Validate device ipaddr success")
#             return CustomResponse.success(message=NOT_FOUND.format(operation_ip, ipaddr))

#         except Exception as err:
#             logger.error("Error validate device ipaddr (Exception): %s", err)
#             return False