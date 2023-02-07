from abc import ABCMeta
from abc import abstractmethod


class AbstractBaseDBClient(metaclass=ABCMeta):

    @property
    @abstractmethod
    def connection(self, *args, **kwargs):
        raise NotImplementedError


