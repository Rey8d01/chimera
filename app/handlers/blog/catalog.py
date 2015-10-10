import re

from tornado.gen import coroutine

import system.handlers
from documents.blog.catalog import CatalogDocument
from documents.blog.post import PostDocument, PostMetaDocument
from system.utils.exceptions import ChimeraHTTPError
from system.components.pagination import Pagination


class CatalogHandler(system.handlers.MainHandler):
    special_aliases = [
        'latest',
        'my',
        'favorite'
    ]

    @coroutine
    def get(self, alias, currentPage):
        """
        Запрос на получение информации по содержимому определенного каталога.

        :param alias:
        :return:
        """
        if alias in self.special_aliases:
            # Для особых псевдонимов генерируем свой набор данных
            count_post = yield PostDocument().objects.count()
            pagination = Pagination(count_post, currentPage, 2)

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

            self.result.update_content({
                "title": u"Последние новости",
                "alias": "latest",
                "posts": list_items_post,
                "pageData": {
                    "currentPage": pagination.current_page,
                    "pageSize": pagination.count_items_on_page,
                    "total": pagination.count_all_items,
                }
            })
        else:
            collection_catalog = yield CatalogDocument().objects.filter({"alias": alias}).find_all()

            if not collection_catalog:
                raise ChimeraHTTPError(404, error_message=u"Коллекция не найдена")
            document_catalog = collection_catalog[0]

            self.result.update_content(document_catalog.to_son())

            count_post = yield PostDocument().objects.filter({PostDocument.aliasCatalog.name: alias}).count()
            pagination = Pagination(count_post, currentPage, 2)

            collection_post = yield PostDocument() \
                .objects \
                .filter({PostDocument.aliasCatalog.name: alias}) \
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

            self.result.update_content({"posts": list_items_post})

        self.write(self.result.get_message())

    @coroutine
    def post(self):
        """
        Создание нового каталога и занесение в базу актуальной по нему информации

        :return:
        """
        pass
        # collection = CatalogDocument().load_post(self)
        # result = yield collection.save()
        # self.write(result)