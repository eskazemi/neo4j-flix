import random
from datetime import datetime
from time import time
from uuid import uuid4, UUID

import pytz as pytz
from fastapi.requests import Request


def get_time() -> datetime:
    """
    Returns the current time.
    Returns:
    """
    return datetime.fromtimestamp(time(), tz=pytz.timezone('Asia/Tehran'))


def get_uuid() -> UUID:
    """Returns an unique UUID (UUID4)"""
    return uuid4()


def is_numeric(_input) -> bool:
    """Returns True if the input is a number."""
    try:
        val = int(_input)
        return True
    except ValueError:
        return False


def get_v_id(prefix: str, prefix_len=2) -> str:
    random.seed(time())
    return str(prefix)[0:prefix_len] + (str(random.random() * 100000)[-5:])


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(str(uuid_to_test), version=version)
    except ValueError:
        return False
    return str(uuid_obj) == str(uuid_to_test)


def get_base_url(request: Request) -> str:
    """
    Returns the base url of the request.

    Parameters
    ----------
    request : Request

    Returns
    -------
    str
    """
    return '{0}://{1}{2}/'.format(request.url.scheme,
                                  request.url.hostname,
                                  ':' + request.url.port.__str__() if request.url.port else '')

