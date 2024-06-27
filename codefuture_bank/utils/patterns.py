from abc import ABC, abstractmethod


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class AbstractFactory(Singleton, ABC):
    @abstractmethod
    def create(self, *args, **kwargs):
        pass
