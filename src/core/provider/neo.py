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
        self.ssc = False
        self.trusted_ca = False
        self.use_neo4j_scheme = True
        try:
            self.__driver = GraphDatabase.driver(self.get_uri(
                self.__uri,
                self.ssc,
                self.trusted_ca,
                self.use_neo4j_scheme),
                auth=(self.__user, self.__pwd))
            self._session_factory = self.__driver.session()

        except Exception as e:
            print("Failed to create the driver:", e)

    @staticmethod
    def get_uri(host, ssc, trusted_ca, use_neo4j_scheme, port=None) -> str:
        """
        Build the uri based on extras
        - Default - uses bolt scheme(bolt://)
        - neo4j_scheme - neo4j://
        - certs_self_signed - neo4j+ssc://
        - certs_trusted_ca - neo4j+s://
        :param port: port
        :param host: host
        :param ssc: ssc( Self signed certificates)
        :param trusted_ca: trusted_ca
        :param use_neo4j_scheme: use_neo4j_scheme
        :return: uri
        """
        scheme = "neo4j" if use_neo4j_scheme else "bolt"

        # Only certificates signed by CA.
        encryption_scheme = ""
        if ssc:
            encryption_scheme = "+ssc"
        elif trusted_ca:
            encryption_scheme = "+s"

        return f"{scheme}{encryption_scheme}://{host}:{7687 if port is None else port} "

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
