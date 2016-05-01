"""Тестовый обработчик основных запросов."""
import json
import system.utils.exceptions
from system.handler import BaseHandler


class TestHandler(BaseHandler):
    """Тестовый обработчик запросов необходим для периодического тестирования работы функций системы."""

    def data_received(self, chunk):
        """
        :param chunk:
        """
        print("data_received")

    async def get(self):
        """Обработчик запроса по методу GET."""
        print("get")
        self.write(json.dumps({"hello": "world"}))

    async def post(self):
        """Обработчик запроса по методу POST."""
        print("post")
        self.write(json.dumps({"hello": "world"}))

    async def put(self):
        """Обработчик запроса по методу PUT."""
        print("put")
        self.write(json.dumps({"hello": "world"}))

    async def delete(self):
        """Обработчик запроса по методу DELETE."""
        print("delete")
        self.write(json.dumps({"hello": "world"}))

    async def head(self):
        """.Обработчик запроса по методу HEAD."""
        print("head")
        self.write(json.dumps({"hello": "world"}))

    async def options(self):
        """Обработчик запроса по методу OPTIONS."""
        print("options")
        self.write(json.dumps({"hello": "world"}))

    async def patch(self):
        """Обработчик запроса по методу PATCH."""
        print("patch")
        self.write(json.dumps({"hello": "world"}))
