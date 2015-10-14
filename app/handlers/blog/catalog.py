"""Обработчики каталогов.

Осуществляют вывод информации по категориям и связанную с ними информацию (записи постов),
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
    """Обработчик запросов для создания/редактирования информации по каталогам.

    POST - Создание нового каталога возможно при отсутствии заданного псевдонима в базе данных.
    PUT - Редактирование нового каталога по заданному и существующему псевдониму в базе данных.

    """

    @coroutine
    def post(self):
        """Создание нового каталога и занесение в базу актуальной по нему информации."""
        alias = self.get_argument(CatalogDocument.alias.name)

        # Проверка наличия каталога с указанным псевдонимом.
        count_catalogs = yield CatalogDocument() \
            .objects \
            .filter({CatalogDocument.alias.name: alias}) \
            .count()
        if count_catalogs > 0:
            raise system.utils.exceptions.ErrorResult(error="Коллекция с таким псевдонимом уже существует")

        document_catalog = CatalogDocument()
        document_catalog.fill_document_from_dict(self.request.arguments)

        yield document_catalog.save()

        raise system.utils.exceptions.Result(content=document_catalog.to_son())

    @coroutine
    def put(self):
        """Изменение существующего каталога."""
        alias = self.get_argument(CatalogDocument.alias.name)

        # Выбор каталога с указанным псевдонимом (иначе исключение).
        collection_catalog = yield CatalogDocument() \
            .objects \
            .filter({CatalogDocument.alias.name: alias}) \
            .limit(1) \
            .find_all()
        if not collection_catalog:
            raise system.utils.exceptions.NotFound(error="Коллекция не найдена")

        document_catalog = collection_catalog[-1]
        document_catalog.fill_document_from_dict(self.request.arguments)
        yield document_catalog.save()

        raise system.utils.exceptions.Result(content=document_catalog.to_son())


class CatalogItemHandler(system.handler.BaseHandler):
    """Обработчик запросов для указанного каталога.

    GET - Запрос информации по заданному псевдониму (с постраничной навигацией).

    :type special_aliases: list Список зарезервированных имен псевдонимов, которые нельзя использовать.
    """

    special_aliases = [
        'latest',
        'my',
        'favorite'
    ]

    @coroutine
    def get(self, alias: str, current_page: int):
        """Запрос на получение информации по содержимому определенного каталога.

        :param alias: Имя псевдонима каталога;
        :type alias: str
        :param current_page: Номер страницы в списке постов;
        :type current_page: int
        """
        result = {}

        if alias in self.special_aliases:
            # Для особых псевдонимов генерируем свой набор данных.
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
            collection_catalog = yield CatalogDocument() \
                .objects \
                .filter({CatalogDocument.alias.name: alias}) \
                .find_all()

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
                    # Обрезание текста для превью.
                    pattern = re.compile(r'<.*?>')
                    clear_text = pattern.sub('', document_post.text)
                    clipped_text = re.split('\s+', clear_text)[:10]

                    document_post.text = " ".join(clipped_text)

                    list_items_post.append(document_post.to_son())

            result.update({"posts": list_items_post})

        raise system.utils.exceptions.Result(content=result)


class CatalogListMainHandler(system.handler.BaseHandler):
    """Обработчик запросов для работы со списком каталогов у которых нет родительского каталога (корень).

    GET - Запрос информации по всем каталогам.

    """

    @coroutine
    def get(self):
        """Вернет список корневых каталогов."""
        collection_catalog = yield CatalogDocument() \
            .objects \
            .filter({CatalogDocument.parentAlias.name: "None"}) \
            .find_all()

        list_catalogs = []
        for document_catalog in collection_catalog:
            # К каждому каталогу примешиваем количество сообщений в каталоге.
            count_posts = yield PostDocument().objects.filter({PostDocument.catalogAlias.name: document_catalog.alias}).count()
            result = document_catalog.to_son()
            result["countPosts"] = count_posts
            list_catalogs.append(result)

        raise system.utils.exceptions.Result(content={"catalogs": list_catalogs})


class CatalogListChildrenHandler(system.handler.BaseHandler):
    """Обработчик запросов для работы со списком каталогов, которые относятся к определенному родителю.

    GET - Запрос информации по всем каталогам.

    """

    @coroutine
    def get(self, alias: str):
        """Вернет список дочерних каталогов.

        :param alias: Имя псевдонима родительского каталога;
        :type alias: str
        """
        collection_catalog = yield CatalogDocument() \
            .objects \
            .filter({CatalogDocument.parentAlias.name: alias}) \
            .find_all()

        list_catalogs = []
        for document_catalog in collection_catalog:
            # К каждому каталогу примешиваем количество сообщений в каталоге.
            count_posts = yield PostDocument().objects.filter({PostDocument.catalogAlias.name: document_catalog.alias}).count()
            result = document_catalog.to_son()
            result["countPosts"] = count_posts
            list_catalogs.append(result)

        raise system.utils.exceptions.Result(content={"catalogs": list_catalogs})
