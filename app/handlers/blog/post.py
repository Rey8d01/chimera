__author__ = 'rey'

import tornado.web
from tornado import gen

import system.handlers
from documents.post import PostDocument
from system.utils.exceptions import ChimeraHTTPError


class PostHandler(system.handlers.MainHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, alias):
        """

        :param alias:
        :return:
        """

        collection_post = yield PostDocument()\
            .objects\
            .filter({"alias": alias})\
            .find_all()

        if not collection_post:
            raise ChimeraHTTPError(404, error_message=u"Пост не найден")
        document_post = collection_post[0]

        self.result.update_content(document_post.to_son())
        self.write(self.result.get_message())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        pass
        # post = PostDocument().load_post(self)
        # result = yield post.save()
        # self.write(result)