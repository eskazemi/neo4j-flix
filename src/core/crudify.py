from uuid import UUID
from src.core.utils import get_time, get_v_id
from src.core.exceptions import (
    NotFoundError,
)


class ConfigMongoWriter:
    created_at: bool = True
    updated_at: bool = True
    has_owner: bool = True
    init_id: bool = True
    init_v_id: bool = False

    def __init__(self, created_at: bool = True, updated_at: bool = True,
                 has_owner: bool = True, init_id: bool = True):
        self.created_at = created_at
        self.updated_at = updated_at
        self.has_owner = has_owner
        self.init_id = init_id


async def neo_inserter(node: str,
                       options: ConfigMongoWriter = ConfigMongoWriter()):
    """
    Inserts data into collection
    """
    pass


async def neo_updater(options: ConfigMongoWriter = ConfigMongoWriter(
    created_at=False, has_owner=False), getter=None):
    """
    Updates data in collection
    """
    pass


async def neo_soft_deleter(query: dict | UUID, node: str):
    """
    Updates data in collection
    """
    pass


async def neo_find_one(query: dict | UUID, node: str) -> dict:
    """
     Ge
     """
    pass


async def neo_find(query: dict | UUID, node: str) -> dict:
    """
     Ge
     """
    pass
