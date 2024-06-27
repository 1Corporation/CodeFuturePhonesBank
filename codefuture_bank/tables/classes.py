from typing import Dict, Tuple

from google_client.classes import GoogleClient
from tables.interfaces import TableManagerInterface, TableInterface, TableFactoryInterface
from tables.models import GoogleTables


class Table(TableInterface):

    def __init__(
            self,
            table_name,
            sheet_id: str,
            sheet_name: str,
            fcs_column: int,
            phone_column: int,
            status_column: int
    ):
        self.__table_name: int = table_name
        self.__sheet_id: str = sheet_id
        self.__sheet_name: str = sheet_name
        self.__fcs_column: int = fcs_column
        self.__phone_column: int = phone_column
        self.__status_column: int = status_column

    def set_value(self, row: int, column: int, value: str):
        client = GoogleClient()
        client.write_data(row, column, value, self.__sheet_id, self.__sheet_name)

    def get_row(self, row: int):
        client = GoogleClient()
        row = client.read_row(row, self.__sheet_id, self.__sheet_name)
        return {
            "fsc": row[self.__fcs_column],
            "phone": row[self.__phone_column],
            "status": row[self.__status_column]
        }

    @property
    def table_name(self):
        return self.__table_name


class TableManager(TableManagerInterface):

    def __init__(self):
        super().__init__()
        self.__tables: Dict[str, TableInterface] = {}

    def get_table(self, table_name: str):
        table = self.__tables.get(table_name)

        if table is None:
            raise ValueError(f'Table {table_name} does not exist')

        return table

    def new_table(self, table: TableInterface):
        if self.__tables.get(table.table_name) is not None:
            raise ValueError(f'Table {table.table_name} already exists')

        self.__tables[table.table_name] = table
        return table


class TableFactory(TableFactoryInterface):
    def create(self, *args: Tuple[str, str, str, int, int, int], **kwargs):
        """
        Create a table

        Args:
            *args: A tuple containing the following arguments:
                - table_name: str,
                - sheet_id: str,
                - sheet_name: str,
                - fcs_column: int,
                - hone_column: int,
                - status_column: int
        """

        table = Table(*args)
        google_table = GoogleTables(*args)
        google_table.save()
        TableManager().new_table(table)

        return table
