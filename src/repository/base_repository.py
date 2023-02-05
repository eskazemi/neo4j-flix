from typing import Callable
from contextlib import AbstractContextManager
from neo4j import Session


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
