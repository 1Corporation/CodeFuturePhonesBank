from abc import ABC, abstractmethod

from utils.patterns import AbstractFactoryInterface, BaseManagerInterface


class StudentInterface(ABC):
    @property
    @abstractmethod
    def telegram_id(self):
        pass

    @property
    @abstractmethod
    def username(self):
        pass

    @property
    @abstractmethod
    def phone(self):
        pass

    @property
    @abstractmethod
    def fcs(self):
        pass


class StudentInteratorFactoryInterface(AbstractFactoryInterface):
    pass


class StudentIteratorInterface(ABC):
    @abstractmethod
    def next(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def row(self):
        pass


class StudentIteratorManagerInterface(BaseManagerInterface):
    pass

