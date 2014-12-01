__author__ = 'rey'

from system.base.handler import BaseHandler
from models.collection import CollectionModel
from models.post import PostModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError
from system.components.pagination import Pagination

import re


class CollectionHandler(BaseHandler):
    special_slugs = [
        'latest'
    ]

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug, currentPage):
        """

        :param slug:
        :return:
        """
        post = PostModel()

        if slug in self.special_slugs:
            # Для особых слагов генерируем свой набор данных
            count_documents_post = yield post.find().count()
            pagination = Pagination(count_documents_post, currentPage, 2)

            documents_post = post.find().sort([("meta.dateCreate", -1)]).limit(pagination.count_items_on_page).skip(pagination.skip_items)

            list_items_post = []
            while (yield documents_post.fetch_next):
                document_post = documents_post.next_object()

                pattern = re.compile(r'<.*?>')
                text = pattern.sub('', document_post["text"])
                print(text)

                post.fill_from_document(document_post)
                list_items_post.append(post.get_data())

            self.result.update_content({
                "title": u"Последние новости",
                "slug": "latest",
                "posts": list_items_post,
                "pageData": {
                    "currentPage": pagination.current_page,
                    "pageSize": pagination.count_items_on_page,
                    "total": pagination.count_all_items,
                }
            })
        else:
            collection = CollectionModel()
            document_collection = yield collection.one({"slug": slug})

            if not document_collection:
                raise ChimeraHTTPError(404, error_message=u"Коллекция не найдена")

            collection.fill_from_document(document_collection)
            self.result.update_content(collection.get_data())

            count_documents_post = yield post.find({"slugCollection": slug}).count()
            pagination = Pagination(count_documents_post, currentPage, 2)

            documents_post = post.find({"slugCollection": slug}).sort([("meta.dateCreate", -1)]).limit(pagination.count_items_on_page).skip(pagination.skip_items)

            list_items_post = []
            if documents_post:
                while (yield documents_post.fetch_next):
                    document_post = documents_post.next_object()
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
        collection = CollectionModel().load_post(self)
        result = yield collection.save()
        self.write(result)