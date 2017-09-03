"""Blog repositories.

DataMapper

"""

from typing import List, Union

from motor.motor_tornado import MotorClient

from .domains import Post


class PostRepository:
    """Репозиторий для работы с коллекцией постов в БД."""

    def __init__(self, client_motor: MotorClient):
        self.__client_motor = client_motor
        self.__collection_name = "post"

    async def get_item_post(self, filters: dict = None) -> Union[Post, None]:
        """Вернет один экземпляр поста, по переданным фильтрам."""

        collection = self.__client_motor[self.__collection_name]
        document = await collection.find_one(filters)

        return Post(**document) if document else None

    async def get_list_posts(self, alias_tag: str = "", user_id: str = "") -> List[Post]:
        """Вернет список постов по зададнным фильтрам."""

        collection = self.__client_motor[self.__collection_name]
        # todo
        find_filter = {}
        if alias_tag:
            find_filter = {"alias": alias_tag}
        if user_id:
            find_filter = {"title": user_id}

        list_posts = []
        if find_filter:
            cursor = collection.find(find_filter)
            for document in (await cursor.to_list(length=100)):
                list_posts.append(Post(**document))

        return list_posts

    async def create_post(self, post: Post = None) -> Union[Post, None]:
        """Создаст в коллекции пост и вернет его экземпляр."""
        if not post:
            return None

        collection = self.__client_motor[self.__collection_name]

        check_exists_post = await self.get_item_post(filters={"alias": post.alias})
        if check_exists_post:
            return None

        post_id = await collection.insert(post.to_dict())
        actual_post = await self.get_item_post(filters={"_id": post_id})
        return actual_post

    async def update_post(self, post: Post = None) -> bool:
        """Обновит в коллекции пост и вернет его обновленный экземпляр."""
        if not post:
            return False

        collection = self.__client_motor[self.__collection_name]

        check_exists_post = await self.get_item_post(filters={"alias": post.alias})
        if not check_exists_post:
            return False

        result = await collection.replace_one({"alias": post.alias}, post.to_dict())
        return bool(result)

    async def delete_post(self, alias: str) -> bool:
        """Обновит в коллекции пост и вернет его обновленный экземпляр."""
        if not alias:
            return False

        collection = self.__client_motor[self.__collection_name]

        check_exists_post = await self.get_item_post(filters={"alias": alias})
        if not check_exists_post:
            return False

        result = await collection.delete_one({"alias": alias})
        return bool(result)
