__author__ = 'rey'

from system.handlers import BaseHandler
# from models.collection import CollectionModel

import tornado.web
from tornado import gen


class ProcessHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, alias):
        """

        :param alias:
        :return:
        """
        self.write("1")

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """

        :return:
        """
        self.write("2")