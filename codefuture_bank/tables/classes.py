from typing import Dict

from django.db.utils import OperationalError

from google_client.classes import GoogleClient
from tables.interfaces import TableManagerInterface, TableInterface, TableFactoryInterface
from tables.models import GoogleTables
from utils.patterns import Singleton


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
            "fcs": row[self.__fcs_column],
            "phone": row[self.__phone_column],
            "status": row[self.__status_column]
        }

    def set_status(self, row: int, value: str):
        self.set_value(row, self.__status_column, value)

    @property
    def table_name(self):
        return self.__table_name

    @property
    def phone_col(self):
        return self.__phone_column

    @property
    def fcs_col(self):
        return self.__fcs_column


class TableManager(TableManagerInterface, Singleton):

    def init(self):
        self.__tables: Dict[str, TableInterface] = {}

    def get(self, key: str, *args, **kwargs):
        table = self.__tables.get(key)

        if table is None:
            raise ValueError(f'Table {key} does not exist')

        return table

    def new(self, table: TableInterface, *args, **kwargs):
        if self.__tables.get(table.table_name) is not None:
            raise ValueError(f'Table {table.table_name} already exists')

        self.__tables[table.table_name] = table
        return table


class TableFactory(TableFactoryInterface, Singleton):

    def init(self, *args, **kwargs):
        tables = GoogleTables.objects.all()
        for table in tables:
            self.create(table.name, table.sheet_id, table.sheet_name, table.fcs_column, table.phone_column,
                        table.status_column)

    def create(self, table_name: str, sheet_id: str, sheet_name: str, fcs_column: int, phone_column: int,
               status_column: int, *args: object, **kwargs: object) -> object:
        table = Table(table_name, sheet_id, sheet_name, fcs_column, phone_column, status_column)

        if not GoogleTables.objects.filter(name=table_name).exists():
            google_table = GoogleTables(name=table_name, sheet_id=sheet_id, sheet_name=sheet_name,
                                        fcs_column=fcs_column,
                                        phone_column=phone_column, status_column=status_column)
            google_table.save()

        TableManager().new(table)

        return table


try:
    TableFactory()
except OperationalError:
    pass
