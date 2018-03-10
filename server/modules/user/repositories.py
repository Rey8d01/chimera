"""Репозитории запросов пользовательской информации."""
import hashlib
import typing
from datetime import datetime

from motor.motor_tornado import MotorClient

import utils.naming
from .domains import DetailInfo, MetaInfo, User


class UserRepository:
    """Репозиторий для работы с коллекцией постов в БД."""

    def __init__(self, client_motor: MotorClient):
        self.__client_motor = client_motor
        self.__collection_name = "user"

    async def get_user(self, filters: dict = None) -> typing.Optional[User]:
        """Вернет объект пользователя по заданным фильтрам."""
        collection = self.__client_motor[self.__collection_name]
        document = await collection.find_one(filters)

        return User(**utils.naming.change_dict_naming_convention(document, utils.naming.camel_2_under)) if document else None

    async def create_user(self, login: str, password: str) -> typing.Optional[User]:
        """Создание нового пользователя."""
        collection = self.__client_motor[self.__collection_name]

        check_exists_user = await self.get_user(filters={"metaInfo.login": login})
        if check_exists_user:
            return None

        detail_info = DetailInfo(data={})
        meta_info = MetaInfo(
            date_registration=datetime.utcnow(),
            date_last_activity=datetime.utcnow(),
            login=login,
            password=hashlib.sha512(password.encode()).hexdigest(),
        )

        user = User(detail_info=detail_info, meta_info=meta_info, list_oauth_info=[])

        document = utils.naming.change_dict_naming_convention(user.to_dict(), utils.naming.under_2_camel)
        user_id = await collection.insert(document)
        actual_user = await self.get_user(filters={"_id": user_id})
        return actual_user

    async def check_user(self, login: str, password: str) -> typing.Optional[User]:
        """Проверка авторизационных данных пользователя."""
        collection = self.__client_motor[self.__collection_name]

        actual_user = await self.get_user(filters={"metaInfo.login": login})
        if not actual_user:
            return None

        if hashlib.sha512(password.encode()).hexdigest() != actual_user.meta_info.password:
            return None

        actual_user.meta_info.date_last_activity = datetime.utcnow()

        document = utils.naming.change_dict_naming_convention(actual_user.to_dict(), utils.naming.under_2_camel)
        result = await collection.replace_one({"metaInfo.login": login}, document)
        return actual_user
