"""Blog handlers."""

from graphql.execution.executors.asyncio import AsyncioExecutor
from utils.exceptions import Response
from utils.handler import BaseHandler
from .schema import schema_blog


class BlogHandler(BaseHandler):
    """Общая обработка всех запросов для блога.

    http://graphql.org/learn/serving-over-http/#http-methods-headers-and-body

    """

    async def get(self):
        """GraphQL GET - запрос данных.

        http://graphql.org/learn/serving-over-http/#get-request
        http://graphql.org/learn/queries/#arguments

        """
        query = self.get_argument(name="query")

        # result = schema_blog.execute(
        #     request_string=query,
        #     executor=AsyncioExecutor(),
        # )

        result = await schema_blog.execute(
            request_string=query,
            executor=AsyncioExecutor(),
            return_promise=True
        )

        raise Response(result)

    async def post(self):
        """GraphQL POST - модификация данных.

        http://graphql.org/learn/serving-over-http/#post-request
        http://graphql.org/learn/queries/#variables

        """
        request = self.get_bytes_body_source()
        query = request.get("query", "")
        operation_name = request.get("operationName", "")
        variables = request.get("variables", {})

        result = await schema_blog.execute(
            request_string=query,
            operation_name=operation_name,
            variable_values=variables,
            executor=AsyncioExecutor(),
            return_promise=True
        )

        raise Response(result)
