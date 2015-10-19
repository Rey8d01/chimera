from system.handler import BaseHandler
from tornado.gen import coroutine


class ProcessHandler(BaseHandler):

    @coroutine
    def get(self, alias):
        """

        :param alias:
        :return:
        """
        self.write("1")

    @coroutine
    def post(self):
        """

        :return:
        """
        self.write("2")