"""Тестовый обработчик основных запросов."""
import utils.exceptions
from utils.handler import BaseHandler


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


import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor

class Query(graphene.ObjectType):
    hello = graphene.String()
    halo = graphene.String()
    name = graphene.String()
    hashtags = graphene.List(graphene.String, l=graphene.Int(), text=graphene.String())

    async def resolve_hello(self, args, context, info):
        return 'World'

    def resolve_halo(self, args, context, info):
        return 'wars II'

    def resolve_name(self, args, context, info):
        return context.get('name')

    def resolve_hashtags(self, args, context, info):
        print(args, context, info)
        l = args.get("l")
        text = args.get("text")
        # 1
        import re
        import transliterate
        raw_tags = re.findall("[^\\\]#[\w-]+", text)
        tags = []
        for raw_tag in raw_tags:
            tag = raw_tag[raw_tag.find("#") + 1:].lower()
            alias = transliterate.slugify(tag) if transliterate.detect_language(tag) else tag
            document_tag = dict(title=tag, alias=alias)
            tags.append(document_tag)
        # 2
        # print(tags)
        return tags[:l]

schema = graphene.Schema(query=Query)


class TestGraphQLHandler(BaseHandler):
    """Тестовый обработчик запросов необходим для периодического тестирования работы функций системы."""

    async def get(self):
        """Обработчик запроса по методу GET."""
        graphql = self.get_argument(name="graphql")
        result = schema.execute(graphql, executor=AsyncioExecutor())
        raise utils.exceptions.Response(result)

    async def post(self):
        """Обработчик запроса по методу POST."""
        # result = schema.execute('{ name }', context_value={'name': 'Syrus'})
        request = self.get_bytes_body_source()
        query = request.get("query", "")
        operation_name = request.get("operationName", "")
        variables = request.get("variables", {})
        result = schema.execute(request_string=query, operation_name=operation_name, variable_values=variables)
        raise utils.exceptions.Response(result)
