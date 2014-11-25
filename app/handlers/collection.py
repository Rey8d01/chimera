__author__ = 'rey'

from system.base.handler import BaseHandler
from models.collection import CollectionModel
from models.post import PostModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError
from system.components.pagination import Pagination


class CollectionHandler(BaseHandler):
    special_slugs = [
        'latest'
    ]

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug, page):
        """

        :param slug:
        :return:
        """
        if slug in self.special_slugs:
            # Для особых слагов генерируем свой набор данных
            post = PostModel()
            documents_post = post.find().sort([('meta.dateCreate', -1)]).limit(1)

            list_items_post = []
            while (yield documents_post.fetch_next):
                document_post = documents_post.next_object()
                post.fill_from_document(document_post)
                list_items_post.append(post.get_data())

            count_documents_post = yield post.find().count()

            # pagination = Pagination(count_documents_post, page)
            pagination = Pagination(110, 9)

            self.result.update_content({
                "title": u"Последние новости",
                "slug": "latest",
                "posts": list_items_post,
                "pageData": {
                    "currentPage": pagination.current_page,
                    "pages": pagination.get_pages()
                }
            })
        else:
            collection = CollectionModel()
            document_collection = yield collection.one({'slug': slug})

            if not document_collection:
                raise ChimeraHTTPError(404, error_message=u"Коллекция не найдена")

            collection.fill_from_document(document_collection)
            self.result.update_content(collection.get_data())

            post = PostModel()
            documents_post = post.find({'slugCollection': slug}).sort([('meta.dateCreate', -1)]).limit(1)

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