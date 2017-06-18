"""Blog schema GraphQL."""

from graphene import Schema, ObjectType, Field, String, Int, List, Boolean, resolve_only_args
from tornado.platform.asyncio import to_asyncio_future
from utils.ca import ErrorResponse
from .blogql.schema import BlogQuery
from .user.schema import UserQuery


class MainQuery(ObjectType):
    """Обработка всех запросов GraphQL к модулям."""

    user = Field(UserQuery)
    blog = Field(BlogQuery)

    async def resolve_user(self, args, context, info):
        """UserQuery."""
        return UserQuery()

    async def resolve_blog(self, args, context, info):
        """BlogQuery."""
        return BlogQuery()

main_schema = Schema(query=MainQuery)
