"""Blog repositories.

DataMapper

"""

from typing import Union, List
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

        collection = database[self.__collection_name]
        document = await collection.find_one(filters)

        return Post(**document) if document else None

    async def get_list_posts(self, alias_tag: str = "", user_id: str = "") -> List[Post]:
        """Вернет список постов по зададнным фильтрам."""
        # if not filters:
        #     return self._entries[-1] if self._entries else None

        collection = database[self.__collection_name]
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

        collection = database[self.__collection_name]

        check_exists_post = await self.get_item_post(filters={"alias": post.alias})
        if check_exists_post:
            return None

        post_id = await collection.insert(post.to_dict())
        actual_post = await self.get_item_post(filters={"_id": post_id})
        return actual_post
