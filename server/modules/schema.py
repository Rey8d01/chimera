"""Main schema GraphQL."""

from graphene import Field, ObjectType, Schema

from .blogql.schema import BlogQuery
from .user.schema import UserQuery


class MainQuery(ObjectType):
    """Обработка всех запросов GraphQL к модулям."""

    user = Field(UserQuery)
    blog = Field(BlogQuery)

    async def resolve_user(self, args, context, info):
        """Resolver UserQuery."""
        return UserQuery()

    async def resolve_blog(self, args, context, info):
        """Resolver BlogQuery."""
        return BlogQuery()


main_schema = Schema(query=MainQuery)
