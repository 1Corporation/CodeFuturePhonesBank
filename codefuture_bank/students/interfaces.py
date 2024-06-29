from abc import ABC, abstractmethod

from utils.patterns import AbstractFactoryInterface, BaseManagerInterface


class StudentInterface(ABC):
    @abstractmethod
    @property
    def telegram_id(self):
        pass

    @abstractmethod
    @property
    def username(self):
        pass

    @abstractmethod
    @property
    def phone(self):
        pass

    @abstractmethod
    @property
    def fcs(self):
        pass


class StudentInteratorFactoryInterface(AbstractFactoryInterface):
    pass


class StudentIteratorInterface(ABC):
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    @property
    def name(self):
        pass


class StudentIteratorManagerInterface(BaseManagerInterface):
    pass

