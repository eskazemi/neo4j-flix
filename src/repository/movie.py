from typing import Callable
from contextlib import AbstractContextManager
from neo4j import Session
from base_repository import BaseRepository


class MovieRepository(BaseRepository):
    NODE_NAME = "Movie"

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory)