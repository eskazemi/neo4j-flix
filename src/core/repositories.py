from abc import ABCMeta
from abc import abstractmethod


class BaseReadOnlyRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def filter(self, key: str, condition: str, value: str):
        raise NotImplementedError


class BaseManageableRepository(BaseReadOnlyRepository, metaclass=ABCMeta):

    @property
    @abstractmethod
    def db(self):
        raise NotImplementedError

    @abstractmethod
    def insert(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, uuid: str, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, uuid: str):
        raise
