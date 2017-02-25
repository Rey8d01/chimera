"""Тестовый обработчик основных запросов."""
import utils.exceptions
from components.handler import BaseHandler


class TestHandler(BaseHandler):
    """Тестовый обработчик запросов необходим для периодического тестирования работы функций системы."""

    def data_received(self, chunk):
        """
        :param chunk:
        """
        print("data_received")

    async def get(self):
        """Обработчик запроса по методу GET."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "GET"})

    async def post(self):
        """Обработчик запроса по методу POST."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "POST"})

    async def put(self):
        """Обработчик запроса по методу PUT."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "PUT"})

    async def delete(self):
        """Обработчик запроса по методу DELETE."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "DELETE"})

    async def head(self):
        """.Обработчик запроса по методу HEAD."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "HEAD"})

    async def options(self):
        """Обработчик запроса по методу OPTIONS."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "OPTIONS"})

    async def patch(self):
        """Обработчик запроса по методу PATCH."""
        raise utils.exceptions.Result(content={"hello": "world", "method": "PATCH"})
