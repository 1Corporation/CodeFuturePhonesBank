from abc import ABC, abstractmethod
from typing import Dict

from utils.patterns import AbstractFactory, Singleton


class TableInterface(ABC):
    @abstractmethod
    def get_row(self, row: int):
        pass

    @abstractmethod
    def set_value(self, row: int, column: int, value: str):
        pass

    @abstractmethod
    @property
    def table_name(self):
        pass


class TableManagerInterface(ABC, Singleton):

    @abstractmethod
    def new_table(self, table: TableInterface):
        pass

    @abstractmethod
    def get_table(self, table_name: str):
        pass


class TableFactoryInterface(AbstractFactory, Singleton):
    pass
