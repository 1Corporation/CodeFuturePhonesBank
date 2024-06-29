from students import interfaces
from typing import Optional, Dict

from tables.interfaces import TableInterface
from students.models import Students
from serializers.serializers import phone_serializer, fcs_serializer


class Student(interfaces.StudentInterface):
    def __init__(self, telegram_id: Optional[int], username: Optional[str], phone: str, fcs: str):
        self.__telegram_id = telegram_id
        self.__username = username
        self.__phone = phone
        self.__fcs = fcs

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


class BaseStudentsIterator(interfaces.StudentIteratorInterface):

    def __init__(self, name, table: TableInterface):
        self.__name = name
        self.__table = table
        self.__row: int = 1

    @property
    def name(self):
        return self.__name

    def get_row(self):

        row = self.__table.get_row(self.__row)
        assert row.get("fcs"), "Iterator is over"

        return row

    def get_student(self, row: list):

        phone = phone_serializer(row[self.__table.phone_col])
        fcs = fcs_serializer(row[self.__table.fcs_col])

        try:
            student = Students.objects.get(phone=phone_serializer(phone))
            return Student(student.telegram_id, student.username, student.phone, student.fcs)

        except Students.DoesNotExist:
            return Student(None, None, phone, fcs)

    def next(self):
        pass


class AllStudentsIterator(BaseStudentsIterator):
    def next(self):
        self.__row += 1
        return self.get_student(self.get_row())


class InDatabaseOnlyIterator(BaseStudentsIterator):
    def next(self):
        while True:
            student = self.get_student(self.get_row())
            if student.telegram_id is None:
                self.__row += 1
                continue
            self.__row += 1
            return student


class NotInDatabaseOnlyIterator(BaseStudentsIterator):
    def next(self):
        while True:
            student = self.get_student(self.get_row())
            if student.telegram_id is not None:
                self.__row += 1
                continue
            self.__row += 1
            return student


class StudentsIteratorFactory(interfaces.StudentInteratorFactoryInterface):

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


class StudentsIteratorManager(interfaces.StudentIteratorManagerInterface):

    def init(self, *args, **kwargs):
        self.__iterators: Dict[str, interfaces.StudentIteratorInterface] = {}

    def get(self, key, *args, **kwargs):
        table = self.__iterators.get(key)

        if table is None:
            raise ValueError(f'Table {key} does not exist')

        return table

    def new(self, iterator: interfaces.StudentIteratorInterface, *args, **kwargs):
        if self.__iterators.get(iterator.name) is not None:
            raise ValueError(f'Table {iterator.name} already exists')

        self.__iterators[iterator.name] = iterator
        return iterator
