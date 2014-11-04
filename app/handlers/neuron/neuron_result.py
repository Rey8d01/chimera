__author__ = 'rey'

from system.base.handler import BaseHandler
# from models.collection import CollectionModel

import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError


class NeuronResultHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug):
        """

        :param slug:
        :return:
        """
        self.write(1)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """

        :return:
        """
        self.write(2)