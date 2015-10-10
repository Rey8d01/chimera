"""
Тестовый обработчик основных запросов.
"""

import json
from system.handler import BaseHandler
from tornado.gen import coroutine


class TestHandler(BaseHandler):
    """
    Тестовый обработчик запросов необходим для периодического тестирования работы функций системы
    """

    def data_received(self, chunk):
        """
        :param chunk:
        """
        print("data_received")

    @coroutine
    def get(self):
        """
        Обработчик запроса по методу GET
        """

        print("get")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def post(self):
        """
        Обработчик запроса по методу POST
        """

        print("post")

        data = self.request.arguments
        print(data)

        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def put(self):
        """
        Обработчик запроса по методу PUT
        """

        print("put")

        data = self.request.arguments
        print(data)

        # import documents.blog.catalog
        #
        # document_catalog = documents.blog.catalog.CatalogDocument()
        # document_catalog.alias = "pseudo"
        # document_catalog.title = "Псевдо"
        # result = yield document_catalog.save()
        # print(result)

        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def delete(self):
        """
        Обработчик запроса по методу DELETE
        """

        print("delete")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def head(self):
        """
        Обработчик запроса по методу HEAD
        """

        print("head")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def options(self):
        """
        Обработчик запроса по методу OPTIONS
        """

        print("options")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def patch(self):
        """
        Обработчик запроса по методу PATCH
        """

        print("patch")
        self.write(json.dumps({"hello": "world"}))
