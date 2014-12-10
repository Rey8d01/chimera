__author__ = 'rey'

import re

import tornado.web
from tornado import gen

import system.handlers
from models.catalog import CatalogModel
from models.post import PostModel
from system.utils.exceptions import ChimeraHTTPError
from system.components.pagination import Pagination


class CatalogHandler(system.handlers.MainHandler):
    special_aliases = [
        'latest'
    ]

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, alias, currentPage):
        """

        :param alias:
        :return:
        """
        post = PostModel()

        if alias in self.special_aliases:
            # Для особых слагов генерируем свой набор данных
            count_documents_post = yield post.find().count()
            pagination = Pagination(count_documents_post, currentPage, 2)

            documents_post = post.find().sort([("meta.dateCreate", -1)]).limit(pagination.count_items_on_page).skip(pagination.skip_items)

            list_items_post = []
            while (yield documents_post.fetch_next):
                document_post = documents_post.next_object()

                pattern = re.compile(r'<.*?>')
                clear_text = pattern.sub('', document_post["text"])
                clipped_text = re.split('\s+', clear_text)[:10]

                document_post["text"] = " ".join(clipped_text)

                post.fill_from_document(document_post)
                list_items_post.append(post.get_data())

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
            collection = CatalogModel()
            document_collection = yield collection.one({"alias": alias})

            if not document_collection:
                raise ChimeraHTTPError(404, error_message=u"Коллекция не найдена")

            collection.fill_from_document(document_collection)
            self.result.update_content(collection.get_data())

            count_documents_post = yield post.find({"aliasCollection": alias}).count()
            pagination = Pagination(count_documents_post, currentPage, 2)

            documents_post = post.find({"aliasCollection": alias}).sort([("meta.dateCreate", -1)]).limit(pagination.count_items_on_page).skip(pagination.skip_items)

            list_items_post = []
            if documents_post:
                while (yield documents_post.fetch_next):
                    document_post = documents_post.next_object()

                    pattern = re.compile(r'<.*?>')
                    clear_text = pattern.sub('', document_post["text"])
                    clipped_text = re.split('\s+', clear_text)[:10]

                    document_post["text"] = " ".join(clipped_text)

                    post.fill_from_document(document_post)
                    list_items_post.append(post.get_data())

            self.result.update_content({"posts": list_items_post})

        self.write(self.result.get_message())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """

        :return:
        """
        collection = CatalogModel().load_post(self)
        result = yield collection.save()
        self.write(result)