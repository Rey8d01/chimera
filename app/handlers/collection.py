__author__ = 'rey'

from system.base.handler import BaseHandler
from models.collection import CollectionModel
from models.post import PostModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError
import json


class CollectionHandler(BaseHandler):
    special_slugs = [
        'latest'
    ]

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug):
        """

        :param slug:
        :return:
        """
        if slug in self.special_slugs:
            # Для особых слагов генерируем свой набор данных
            # special_function = getattr(self, slug)
            # special_function()
            post = PostModel()
            documents_post = post.find().sort([('_id', -1)])

            if not documents_post:
                raise ChimeraHTTPError(404, error_message=u"Последние новости отсутствуют")

            list_items_post = []
            while (yield documents_post.fetch_next):
                document_post = documents_post.next_object()
                post.fill_by_data(document_post)
                list_items_post.append(post.get_data())

            latest = {
                "title": u"Последние новости",
                "slug": "/latest",
                "posts": list_items_post
            }
            self.write(json.dumps(latest))
        else:
            collection = CollectionModel()
            document_collection = yield collection.one({'slug': slug})

            if not document_collection:
                raise ChimeraHTTPError(404, error_message=u"Коллекция не найдена")

            collection.fill_by_data(document_collection)
            self.write(collection.get_json())

    @tornado.web.asynchronous
    @gen.coroutine
    def latest(self):
        """

        :return:
        """
        post = PostModel()
        documents_post = post.find().sort([('_id', -1)])

        if not documents_post:
            raise ChimeraHTTPError(404, error_message=u"Последние новости отсутствуют")

        list_items_post = []
        while (yield documents_post.fetch_next):
            document_post = documents_post.next_object()
            post.fill_by_data(document_post)
            list_items_post.append(post.get_data())

        latest = {
            "title": u"Последние новости",
            "slug": "/latest",
            "posts": list_items_post
        }
        self.write(json.dumps(latest))

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """

        :return:
        """
        collection = CollectionModel().load_post(self)
        result = yield collection.save()
        self.write(result)