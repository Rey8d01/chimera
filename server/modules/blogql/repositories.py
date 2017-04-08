"""Blog repositories."""

from typing import Union

from settings import database
from .domains import Post


class PostRepository:
    """Репозиторий для работы с коллекцией постов в БД."""

    __collection_name = "post"

    _entries = None

    def __init__(self, entries: list = None):
        self._entries = []

        if entries:
            self._entries.extend(entries)

    async def get_item_post(self, filters: dict = None) -> Union[Post, None]:
        """Вернет один экземпляр поста, по переданным фильтрам."""
        if not filters:
            return self._entries[-1] if self._entries else None

        # motor.motor_tornado.MotorCollection
        collection = database[self.__collection_name]
        document = await collection.find_one(filters)

        return Post(**document)

    async def create_post(self, doc: dict = None) -> Union[Post, None]:
        """Создаст в коллекции пост и вернет его экземпляр."""
        if not doc:
            return None

        collection = database[self.__collection_name]
        document = await collection.insert(doc)

        return Post(**document)
