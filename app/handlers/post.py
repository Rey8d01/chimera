__author__ = 'rey'

from system.base.handler import BaseHandler
from models.post import PostModel
import tornado.web
from tornado import gen


class PostHandler(BaseHandler):

    def get(self, id_post):

        post = PostModel()

        self.write(id_post)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        post = PostModel().load_post(self)
        result = yield post.save()
        self.write(result)