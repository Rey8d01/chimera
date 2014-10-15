# Базовая модель через которую будет происходить обращение к базе данных
from symbol import yield_arg

__author__ = 'rey'

import bson
import motor

from system.utils.loader import Loader

from tornado.concurrent import return_future
from tornado import gen


class BaseModel(motor.MotorCollection, Loader):

    _client = motor.MotorClient('localhost', 27017).blog

    _collection = None

    def __init__(self):
        """

        :return:
        """
        self._collection = self.__get_db(self.get_name_collection())

        motor.MotorCollection.__init__(self, self._client, self.get_name_collection())
        Loader.__init__(self)

    def __get_db(self, name):
        """
        Инициализация коллекции для определенной модели
        :param name:
        :return:
        """
        return self._client[name]

    def get_name_collection(self):
        """
        Название коллекции
        :return:
        """
        pass

    def references(self):
        """
        Описание ссылок на другие модели
        :return:
        """
        pass

    def save(self):
        self.insert(self.get_data())

    def one(self, *args, **kwargs):
        return self.find_one(*args, **kwargs)


class ErrorModel(Exception):
    """
    All error class
    """
    pass


class FailedOperationsDB(ErrorModel):
    """
    Operation not executed
    """
    pass


class SuccessOperationDB(ErrorModel):
    """
    Operation completed successfully
    """
    pass