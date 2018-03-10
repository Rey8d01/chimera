"""Main schema GraphQL."""

import graphene

from .blog.schema import BlogQuery, BlogMutation
from .user.schema import UserQuery, UserMutation


class MainQuery(graphene.ObjectType):
    """Обработка всех запросов GraphQL к модулям."""

    # user = graphene.Field(UserQuery)
    blog = graphene.Field(BlogQuery)

    async def resolve_user(self, info, *args, **kwargs):
        """Resolver UserQuery."""
        return UserQuery()

    async def resolve_blog(self, info, *args, **kwargs):
        """Resolver BlogQuery."""
        return BlogQuery()


class MainMutation(graphene.ObjectType):
    """Обработка всех запросов GraphQL к модулям."""

    blog = graphene.Field(BlogMutation)
    user = graphene.Field(UserMutation)

    async def resolve_user(self, info, *args, **kwargs):
        """Resolver UserQuery."""
        return UserMutation()

    async def resolve_blog(self, info, *args, **kwargs):
        """Resolver BlogQuery."""
        return BlogQuery()


main_schema = graphene.Schema(query=MainQuery, mutation=MainMutation)
