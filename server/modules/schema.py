"""Main schema GraphQL."""

from graphene import Field, ObjectType, Schema

from .blogql.schema import BlogQuery
from .user.schema import UserQuery


class MainQuery(ObjectType):
    """Обработка всех запросов GraphQL к модулям."""

    user = Field(UserQuery)
    blog = Field(BlogQuery)

    async def resolve_user(self, info, *args, **kwargs):
        """Resolver UserQuery."""
        return UserQuery()

    async def resolve_blog(self, info, *args, **kwargs):
        """Resolver BlogQuery."""
        return BlogQuery()


main_schema = Schema(query=MainQuery)
