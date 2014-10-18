__author__ = 'rey'

from system.base.handler import BaseHandler
from models.post import PostModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError


class PostHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug):
        """

        :param slug:
        :return:
        """
        post = PostModel()
        document_post = yield post.one({'slug': slug})

        if not document_post:
            raise ChimeraHTTPError(404, error_message=u"Пост не найден")

        post.fill_by_data(document_post)
        self.write(post.get_json())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        post = PostModel().load_post(self)
        result = yield post.save()
        self.write(result)