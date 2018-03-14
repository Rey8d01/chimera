"""Репозитории запросов для блога."""
import typing

from motor.motor_tornado import MotorClient

from utils.db import Repository
from .domains import Post
from ..user.domains import User


class PostRepository(Repository):
    """Репозиторий для работы с коллекцией постов в БД."""

    def __init__(self, client_motor: MotorClient):
        self.__client_motor = client_motor
        self.__collection_name = "post"

    async def get_item_post(self, filters: dict = None) -> typing.Optional[Post]:
        """Вернет один экземпляр поста, по переданным фильтрам."""

        collection = self.__client_motor[self.__collection_name]
        document_post = await collection.find_one(filters)
        if document_post is None:
            return None

        document_user = await self.__client_motor.dereference(document_post["metaInfo"]["user"])
        document_post["metaInfo"]["user"] = User.from_document(document_user)

        return Post.from_document(document_post) if document_post else None

    async def get_list_posts(self, alias_tag: str = "", user_id: str = "") -> typing.List[Post]:
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
                list_posts.append(Post.from_document(document))

        return list_posts

    async def create_post(self, post: Post = None) -> typing.Optional[Post]:
        """Создаст в коллекции пост и вернет его экземпляр."""
        if not post:
            return None

        collection = self.__client_motor[self.__collection_name]

        check_exists_post = await self.get_item_post(filters={"alias": post.alias})
        if check_exists_post:
            return None

        post_id = await collection.insert(self.for_insert(post))
        actual_post = await self.get_item_post(filters={"_id": post_id})
        return actual_post

    async def update_post(self, post: Post = None) -> bool:
        """Обновит в коллекции пост и вернет его обновленный экземпляр."""
        if not post:
            return False

        collection = self.__client_motor[self.__collection_name]

        filters = {
            "alias": post.alias,
            "metaInfo.user.$id": post.meta_info.user._id,
        }
        check_exists_post = await self.get_item_post(filters=filters)
        if not check_exists_post:
            return False

        result = await collection.replace_one({"alias": post.alias}, post.to_document())
        return bool(result)

    async def delete_post(self, alias: str, user: User) -> bool:
        """Обновит в коллекции пост и вернет его обновленный экземпляр."""
        if not alias:
            return False

        collection = self.__client_motor[self.__collection_name]

        filters = {
            "alias": alias,
            "metaInfo.user.$id": user._id,
        }
        check_exists_post = await self.get_item_post(filters=filters)
        if not check_exists_post:
            return False

        result = await collection.delete_one({"alias": alias})
        return bool(result)
