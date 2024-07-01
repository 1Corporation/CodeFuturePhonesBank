from abc import ABC, abstractmethod

from utils.patterns import AbstractFactoryInterface, BaseManagerInterface


class TableInterface(ABC):
    @abstractmethod
    def get_row(self, row: int):
        pass

    @abstractmethod
    def set_value(self, row: int, column: int, value: str):
        pass

    @abstractmethod
    def set_status(self, row: int, statu: str):
        pass

    @property
    @abstractmethod
    def table_name(self):
        pass

    @property
    @abstractmethod
    def fcs_col(self):
        pass

    @property
    @abstractmethod
    def phone_col(self):
        pass


class TableManagerInterface(BaseManagerInterface):
    pass


class TableFactoryInterface(AbstractFactoryInterface):
    pass
