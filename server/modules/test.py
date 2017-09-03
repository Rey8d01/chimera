"""Тестовый обработчик основных запросов."""
import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor

import utils.exceptions
from modules.handler import BaseHandler


class TestRestHandler(BaseHandler):
    """Тестовый обработчик запросов необходим для периодического тестирования работы функций системы."""

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


class Query(graphene.ObjectType):
    hello = graphene.String()
    name = graphene.String()

    async def resolve_hello(self, args, context, info):
        return 'World'

    def resolve_name(self, args, context, info):
        return context.get('name')


schema = graphene.Schema(query=Query)


class TestGraphQLHandler(BaseHandler):
    """Тестовый обработчик запросов необходим для периодического тестирования работы функций системы."""

    async def get(self):
        """Обработчик запроса по методу GET."""
        graphql = self.get_argument(name="graphql")
        # result = schema.execute(graphql, executor=AsyncioExecutor())
        result = await schema.execute(
            request_string=graphql,
            executor=AsyncioExecutor(),
            return_promise=True
        )
        raise utils.exceptions.Response(result)

    async def post(self):
        """Обработчик запроса по методу POST."""
        request = self.get_bytes_body_source()
        query = request.get("query", "")
        operation_name = request.get("operationName", "")
        variables = request.get("variables", {})
        # result = schema.execute(request_string=query, operation_name=operation_name, variable_values=variables)
        result = await schema.execute(
            request_string=query,
            operation_name=operation_name,
            variable_values=variables,
            executor=AsyncioExecutor(),
            return_promise=True
        )
        raise utils.exceptions.Response(result)
