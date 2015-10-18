"""Обработчики для работы с тегами в постах.

Осуществляют вывод постов по тегам, а так же список всех тегов. Теги идентифицируются по их псевдонимам, по ним очуществляется просмотр.

"""
import re
import system.handler
import system.utils.exceptions
from tornado.gen import coroutine
from documents.blog.post import PostDocument, PostMetaDocument, PostTagsDocument
from system.utils.pagination import Pagination


class TagItemHandler(system.handler.BaseHandler):
    """Обработчик запросов для указанного тега.

    GET - Запрос списка постов по заданному тегу (с постраничной навигацией).

    """

    @coroutine
    def get(self, alias: str, current_page: int):
        """Запрос на получение информации по содержимому определенного тега.

        :param alias: Имя псевдонима тега;
        :type alias: str
        :param current_page: Номер страницы в списке постов;
        :type current_page: int
        """
        current_page = int(current_page)
        result = {}

        count_post = yield PostDocument()\
            .objects\
            .filter({PostDocument.tags.name: {"$elemMatch": {PostTagsDocument.alias.name: alias}}}) \
            .count()
        pagination = Pagination(count_post, current_page, 2)

        collection_post = yield PostDocument() \
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

                list_items_post.append(document_post.to_son())

        result.update({"posts": list_items_post})

        raise system.utils.exceptions.Result(content=result)


class TagListHandler(system.handler.BaseHandler):
    """Обработчик запросов для работы со списком каталогов у которых нет родительского каталога (корень).

    GET - Запрос списка всех тегов.

    """

    @coroutine
    def get(self):
        """Вернет список всех тегов."""

        collection_aggregate_tags = yield PostDocument() \
            .objects \
            .aggregate \
            .unwind(PostDocument.tags) \
            .group_by(PostDocument.tags) \
            .fetch()

        list_tags = [item_aggregate_tags[PostDocument.tags.name] for item_aggregate_tags in collection_aggregate_tags]

        raise system.utils.exceptions.Result(content={"tags": list_tags})
