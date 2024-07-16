from students import interfaces
from django.db.utils import OperationalError
from typing import Optional, Dict

from tables.classes import Table
from tables.interfaces import TableInterface
from tables.models import GoogleTables
from students.models import Students
from serializers.serializers import phone_serializer, fcs_serializer
from utils.patterns import Singleton


class Student(interfaces.StudentInterface):
    def __init__(self, telegram_id: Optional[int], username: Optional[str], phone: str, fcs: str):
        self.__telegram_id = telegram_id
        self.__username = username
        self.__phone = phone_serializer(phone)
        self.__fcs = fcs_serializer(fcs)

    @property
    def phone(self):
        return self.__phone

    @property
    def fcs(self):
        return self.__fcs

    @property
    def username(self):
        return self.__username

    @property
    def telegram_id(self):
        return self.__telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id):
        self.__telegram_id = telegram_id

    @username.setter
    def username(self, username):
        self.__username = username

    @fcs.setter
    def fcs(self, fcs):
        self.__fcs = fcs_serializer(fcs)

    @phone.setter
    def phone(self, phone):
        self.__phone = phone_serializer(phone)

    def create_student(self):
        try:
            Students.objects.get(telegram_id=self.telegram_id)
            raise ValueError(f"{self.telegram_id} already exists")
        except Students.DoesNotExist as e:  # TODO: Заменить на ошибку, возникающую при нарушении правила primary key
            student = Students()
            student.telegram_id = self.telegram_id
            student.username = self.username
            student.phone = self.phone
            student.fcs = self.fcs

            student.save()
            return self


class BaseStudentsIterator(interfaces.StudentIteratorInterface):

    def __init__(self, name, table: TableInterface):
        self.__name = name
        self.__table = table
        self.row: int = 1

    @property
    def name(self):
        return self.__name

    def get_row(self):
        row = self.__table.get_row(self.row)
        assert row.get("fcs"), "Iterator is over"

        return row

    def get_student(self, row: dict):
        phone = phone_serializer(row["phone"])
        fcs = fcs_serializer(row["fcs"])

        try:
            student = Students.objects.get(phone=phone)
            return Student(student.telegram_id, student.username, student.phone, student.fcs)

        except Students.DoesNotExist:
            return Student(None, None, phone, fcs)

    def next(self):
        pass


class AllStudentsIterator(BaseStudentsIterator):
    def next(self):
        self.row += 1
        return self.get_student(self.get_row())


class InDatabaseOnlyIterator(BaseStudentsIterator):
    def next(self):
        while True:
            student = self.get_student(self.get_row())
            if student.telegram_id is None:
                self.row += 1
                continue
            self.row += 1
            return student


class NotInDatabaseOnlyIterator(BaseStudentsIterator):
    def next(self):
        while True:
            student = self.get_student(self.get_row())
            if student.telegram_id is not None:
                self.row += 1
                continue
            self.row += 1
            return student


class StudentsIteratorFactory(interfaces.StudentInteratorFactoryInterface, Singleton):

    def init(self):

        super().__init__()
        tables = GoogleTables.objects.all()
        for table in tables:
            table_object = Table(table.name, table.sheet_id, table.sheet_name, table.fcs_column, table.phone_column, table.status_column)
            self.create(table.name, table_object, 'all')

    def create(self, name, table: TableInterface, iter_type: str, *args, **kwargs):
        iterator = None

        match iter_type:
            case 'all':
                iterator = AllStudentsIterator(name, table)
            case 'in_database':
                iterator = InDatabaseOnlyIterator(name, table)
            case 'not_in_database':
                iterator = NotInDatabaseOnlyIterator(name, table)

        StudentsIteratorManager().new(iterator, *args, **kwargs)
        return iterator


class StudentsIteratorManager(interfaces.StudentIteratorManagerInterface, Singleton):

    def init(self, *args, **kwargs):
        self.__iterators: Dict[str, interfaces.StudentIteratorInterface] = {}

    def get(self, key, *args, **kwargs):
        table = self.__iterators.get(key)

        if table is None:
            raise ValueError(f'Table {key} does not exist')

        return table

    def new(self, iterator: interfaces.StudentIteratorInterface, *args, **kwargs):
        if self.__iterators.get(iterator.name) is not None:
            raise ValueError(f'Iterator {iterator.name} already exists')

        self.__iterators[iterator.name] = iterator
        return iterator

try:
    StudentsIteratorFactory()
except OperationalError:
    pass