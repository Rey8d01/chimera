"""Обработчики для работы с тегами в постах.

Осуществляют вывод постов по тегам, а так же список всех тегов. Теги идентифицируются по их псевдонимам, по ним очуществляется просмотр.

"""
import re

import components.handler
import utils.exceptions
from modules.blog.documents.post import PostDocument, PostMetaDocument, PostTagsDocument
from utils.pagination import Pagination


class TagItemHandler(components.handler.MainHandler):
    """Обработчик запросов для указанного тега.

    GET - Запрос списка постов по заданному тегу (с постраничной навигацией).

    """

    async def get(self, alias: str, current_page: int):
        """Запрос на получение информации по содержимому определенного тега.

        :param alias: Имя псевдонима тега;
        :param current_page: Номер страницы в списке постов;
        """
        current_page = int(current_page)
        result = {}

        count_post = await PostDocument()\
            .objects\
            .filter({PostDocument.tags.name: {"$elemMatch": {PostTagsDocument.alias.name: alias}}}) \
            .count()
        pagination = Pagination(count_post, current_page, 5)

        collection_post = await PostDocument() \
            .objects \
            .filter({PostDocument.tags.name: {"$elemMatch": {PostTagsDocument.alias.name: alias}}}) \
            .sort(PostDocument.meta.name + "." + PostMetaDocument.dateCreate.name, direction=-1) \
            .limit(pagination.count_items_on_page) \
            .skip(pagination.skip_items) \
            .find_all()

        list_items_post = []
        if collection_post:
            for document_post in collection_post:
                # Обрезание текста для превью.
                pattern = re.compile(r'<.*?>')
                clear_text = pattern.sub('', document_post.text)
                clipped_text = re.split('\s+', clear_text)[:10]

                document_post.text = " ".join(clipped_text)

                list_items_post.append(document_post.to_json())

        result.update({
            "posts": list_items_post,
            "pageData": {
                "currentPage": pagination.current_page,
                "pageSize": pagination.count_items_on_page,
                "total": pagination.count_all_items,
            }})

        raise utils.exceptions.Result(content=result)


class TagListHandler(components.handler.MainHandler):
    """Обработчик запросов для работы со списком каталогов у которых нет родительского каталога (корень).

    GET - Запрос списка всех тегов.

    """

    async def get(self):
        """Вернет список всех тегов. Теги помещаются в кеш."""
        tags = await self.redis.get("tags")

        # todo поправить при обновлении aggregate в motorengine.
        if tags is None:
            collection_aggregate_tags = PostDocument() \
                .objects \
                .aggregate \
                .unwind(PostDocument.tags) \
                .group_by(PostDocument.tags)

            motor_collection = collection_aggregate_tags.queryset.coll()
            tags = []
            async for item_aggregate_tags in motor_collection.aggregate(collection_aggregate_tags.to_query()):
                tags.append(item_aggregate_tags["_id"][PostDocument.tags.name])

            await self.redis.set("tags", self.escape.json_encode(tags))
        else:
            tags = self.escape.json_decode(self.escape.to_unicode(tags))

        raise utils.exceptions.Result(content={"tags": tags})