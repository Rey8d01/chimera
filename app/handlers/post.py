__author__ = 'rey'

import system.base.handler
from models.post import PostModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError


class PostHandler(system.base.handler.MainHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, alias):
        """

        :param alias:
        :return:
        """
        post = PostModel()
        document_post = yield post.one({'alias': alias})

        if not document_post:
            raise ChimeraHTTPError(404, error_message=u"Пост не найден")

        post.fill_from_document(document_post)
        self.result.update_content(post.get_data())
        self.write(self.result.get_message())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        post = PostModel().load_post(self)
        result = yield post.save()
        self.write(result)