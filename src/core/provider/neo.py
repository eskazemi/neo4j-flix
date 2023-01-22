from typing import Callable
from contextlib import AbstractContextManager, contextmanager
from neo4j import GraphDatabase
from neo4j import Session


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        self._session_factory = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri,
                                                 auth=(self.__user, self.__pwd))
            self._session_factory = self.__driver.session()

        except Exception as e:
            print("Failed to create the driver:", e)

    @contextmanager
    def session(self) -> Callable[
        ..., AbstractContextManager[Session]]:
        """Get the Neo4J context manager"""
        session: Session = self._session_factory
        try:
            yield session
        except Exception:
            raise Exception
        finally:
            session.close()
