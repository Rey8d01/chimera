# Базовая модель через которую будет происходить обращение к базе данных
from symbol import yield_arg

__author__ = 'rey'

import bson
import motor

from system.utils.loader import Loader

from tornado.concurrent import return_future
from tornado import gen
import system.configuration


class BaseDocument(motor.MotorCollection, Loader):
    """
    :todo использовать стандартные декораторы для свойств @property
    """
    _client = None

    _collection = None

    def __init__(self):
        """

        :return:
        """
        self.__get_db()
        self._collection = self.__get_collection(self.get_name_collection())

        motor.MotorCollection.__init__(self, self._client, self.get_name_collection())
        Loader.__init__(self)

    def __get_db(self, db_name=None):
        """

        :param db_name:
        :return:
        """
        if db_name is None:
            db_name = system.configuration.DB_NAME
        self._client = motor.MotorClient(system.configuration.DB_HOST, system.configuration.DB_PORT)[db_name]

    def __get_collection(self, collection_name):
        """
        Инициализация коллекции для определенной модели
        :param collection_name:
        :return:
        """
        return self._client[collection_name]

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