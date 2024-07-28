"""
Logging format and context filter
"""

import logging
import sys
from contextvars import ContextVar
from typing import Optional

import colorlog

LOG_FORMAT = "%(log_color)s %(asctime)s - [%(levelname)s] - %(name)s - "\
    "(%(filename)s).%(funcName)s(%(lineno)d) - C: %(ctx)s - U: %(user)s - M: %(message)s"

correlation_id: ContextVar[Optional[str]] = ContextVar(
    'correlation_id', default=None)

correlation_user: ContextVar[Optional[str]] = ContextVar(
    'correlation_user', default=None)

def set_context(context): # pylint: disable=too-few-public-methods
    """
    Set context
    :param context:
    :return:
    """

    return correlation_id.set(context)

def set_usercontext(context): # pylint: disable=too-few-public-methods
    """
    Set context
    :param context:
    :return:
    """

    return correlation_user.set(context)

def get_context(): # pylint: disable=too-few-public-methods
    """
    Get context
    :return:
    """

    return correlation_id.get()

def get_usercontext(): # pylint: disable=too-few-public-methods
    """
    Get context
    :return:
    """

    return correlation_user.get()


class ContextFilter(logging.Filter): # pylint: disable=too-few-public-methods
    """
    Filter
    """

    def filter(self, record):
        record.user = correlation_user.get()
        record.ctx = correlation_id.get()
        return True


def get_stream_handler():
    """
    Get stream handler
    :return:
    """

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(colorlog.ColoredFormatter(LOG_FORMAT))
    return stream_handler

def get_logger(name):
    """
    Get logger
    :param name:
    :return:
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_stream_handler())
    filter_context = ContextFilter()
    logger.addFilter(filter_context)
    return logger
