"""User repositories."""

from typing import Union, List
from settings import database
from .domains import User, OAuthInfo, MetaInfo, DetailInfo
from datetime import datetime
import hashlib


class UserRepository:
    """Репозиторий для работы с коллекцией постов в БД."""

    __collection_name = "user"

    async def get_user(self, filters: dict = None) -> Union[User, None]:
        collection = database[self.__collection_name]
        document = await collection.find_one(filters)

        return User(**document) if document else None

    async def create_user(self, user: str, password: str) -> Union[User, None]:
        collection = database[self.__collection_name]

        check_exists_user = await self.get_user(filters={"meta_info.user": user})
        if check_exists_user:
            return None

        detail_info = DetailInfo(data={})
        meta_info = MetaInfo(
            date_registration=datetime.utcnow(),
            date_last_activity=datetime.utcnow(),
            user=user,
            password=hashlib.sha512(password.encode()).hexdigest(),
        )

        user = User(detail_info=detail_info, meta_info=meta_info, list_oauth_info=[])

        user_id = await collection.insert(user.to_dict())
        actual_user = await self.get_user(filters={"_id": user_id})
        return actual_user

    async def check_user(self, user: str, password: str) -> Union[User, None]:
        collection = database[self.__collection_name]

        actual_user = await self.get_user(filters={"meta_info.user": user})
        if not actual_user:
            return None

        if hashlib.sha512(password.encode()).hexdigest() != actual_user.meta_info.password:
            return None

        actual_user.meta_info.date_last_activity = datetime.utcnow()

        result = await collection.replace_one({"meta_info.user": user}, actual_user.to_dict())
        return actual_user
