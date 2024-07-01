from abc import ABC, abstractmethod


class SerializerInterface(ABC):
    @abstractmethod
    def __init__(self, row, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def row(self):
        pass


class Serializer(SerializerInterface):

    def __init__(self, row, *args, **kwargs):
        self.__row = row[0]

    @property
    def row(self):
        return self.__row

