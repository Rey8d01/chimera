"""
Обработчики каталогов. Осуществляют вывод информации по категориям и связанную с ними информацию (записи постов),
а так же организует создание и редактирование информации по сущетсвующим каталогам.
Каталоги идентифицируются по их псевдонимам, по ним очуществляется просмотр и редактирование.
"""

import re
import system.handler
import system.utils
import system.utils.exceptions
from tornado.gen import coroutine
from documents.blog.catalog import CatalogDocument
from documents.blog.post import PostDocument, PostMetaDocument
from system.components.pagination import Pagination


class CatalogEditHandler(system.handler.BaseHandler):
    """
    Обработчик запросов для создания/редактирования информации по каталогам.
    Создание нового каталога возможно при отсутствии заданного псевдонима в базе данных.
    """

    @coroutine
    def post(self):
        """
        Создание нового каталога и занесение в базу актуальной по нему информации.
        """

        request_data = self.request.arguments

        document_catalog = CatalogDocument()
        document_catalog.fill_document_from_dict(request_data)

        result = yield document_catalog.save()

        raise system.utils.exceptions.Result(content=result)


class CatalogItemHandler(system.handler.BaseHandler):
    """
    Обработчик запросов для указанного каталога.

    :type special_aliases: list Список зарезервированных имен псевдонимов, которые нельзя использовать.
    """

    special_aliases = [
        'latest',
        'my',
        'favorite'
    ]

    @coroutine
    def get(self, alias: str, current_page: int):
        """
        Запрос на получение информации по содержимому определенного каталога.

        :param alias: Имя псевдонима каталога;
        :type alias: str
        :param current_page: Номер страницы в списке постов;
        :type current_page: int
        """

        result = {}
        if alias in self.special_aliases:
            # Для особых псевдонимов генерируем свой набор данных
            count_post = yield PostDocument().objects.count()
            pagination = Pagination(count_post, current_page, 2)

            collection_post = yield PostDocument() \
                .objects \
                .sort(PostDocument.meta.name + "." + PostMetaDocument.dateCreate.name, direction=1) \
                .limit(pagination.count_items_on_page) \
                .skip(pagination.skip_items) \
                .find_all()

            list_items_post = []
            for document_post in collection_post:
                pattern = re.compile(r'<.*?>')
                clear_text = pattern.sub('', document_post.text)
                clipped_text = re.split('\s+', clear_text)[:10]

                document_post.text = " ".join(clipped_text)

                list_items_post.append(document_post.to_son())

            result.update({
                "title": "Последние новости",
                "alias": "latest",
                "posts": list_items_post,
                "pageData": {
                    "current_page": pagination.current_page,
                    "pageSize": pagination.count_items_on_page,
                    "total": pagination.count_all_items,
                }
            })
        else:
            collection_catalog = yield CatalogDocument().objects.filter({"alias": alias}).find_all()

            if not collection_catalog:
                raise system.utils.exceptions.NotFound(error="Коллекция не найдена")
            document_catalog = collection_catalog[0]

            result.update(document_catalog.to_son())

            count_post = yield PostDocument().objects.filter({PostDocument.catalogAlias.name: alias}).count()
            pagination = Pagination(count_post, current_page, 2)

            collection_post = yield PostDocument() \
                .objects \
                .filter({PostDocument.catalogAlias.name: alias}) \
                .sort(PostDocument.meta.name + "." + PostMetaDocument.dateCreate.name, direction=-1) \
                .limit(pagination.count_items_on_page) \
                .skip(pagination.skip_items) \
                .find_all()

            list_items_post = []
            if collection_post:
                for document_post in collection_post:
                    # Обрезание текста для превью
                    pattern = re.compile(r'<.*?>')
                    clear_text = pattern.sub('', document_post.text)
                    clipped_text = re.split('\s+', clear_text)[:10]

                    document_post.text = " ".join(clipped_text)

                    list_items_post.append(document_post.to_son())

            result.update({"posts": list_items_post})

        raise system.utils.exceptions.Result(content=result)


class CatalogListHandler(system.handler.BaseHandler):
    """
    Обработчик запросов для работы со списком каталогов.
    """

    @coroutine
    def get(self):
        """
        Вернет список каталогов.
        """

        collection_catalog = yield CatalogDocument().objects.find_all()

        list_catalogs = []
        for document_catalog in collection_catalog:
            count_posts = yield PostDocument().objects.filter({PostDocument.catalogAlias.name: document_catalog.alias}).count()
            result = document_catalog.to_son()
            result["countPosts"] = count_posts
            list_catalogs.append(result)

        raise system.utils.exceptions.Result(content={"catalogs": list_catalogs})
