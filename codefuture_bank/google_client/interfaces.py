from abc import ABC, abstractmethod


class GoogleClientInterface(ABC):
    @abstractmethod
    def write_data(self, row, column, data, sheet_id, sheet_name, *args, **kwargs):
        pass

    @abstractmethod
    def read_row(self, row: int, sheet_id, sheet_name, *args, **kwargs) -> list:
        pass
