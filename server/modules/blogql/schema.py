"""Blog schema GraphQL."""

from typing import Union
from graphene import Schema, ObjectType, Field, String, resolve_only_args
from tornado.platform.asyncio import to_asyncio_future

from .use_cases import PostItemUseCase, NewPostUseCase
from .gateways import PostItemRequest, NewPostRequest
from .repositories import PostRepository


class PostObjectType(ObjectType):
    """Схема документа Post для генерации ответов."""

    # id = String()
    alias = String()
    title = String()
    text = String()

    # user = String()
    # author = String()
    # dateCreate = String()
    # dateUpdate = String()
    # tags = List(Episode)

    # def resolve_friends(self, args, *_):
    #     # The character friends is a list of strings
    #     return [get_character(f) for f in self.friends]


class BlogQuery(ObjectType):
    """Обработка запросов блога с использованием GraphQL."""

    post = Field(PostObjectType, alias=String())
    save_post = Field(PostObjectType, alias=String(), title=String(), text=String())

    @resolve_only_args
    async def resolve_post(self, alias: str) -> Union[PostObjectType, bool]:
        """Запрос поста по его псевдониму."""
        request_for_use_case = PostItemRequest(request_data={"alias": alias})
        repository_post = PostRepository()
        use_case_post_item = PostItemUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_post_item.execute(request_object=request_for_use_case))

        if not bool(response_from_use_case):
            return False

        return PostObjectType(
            alias=response_from_use_case.value.alias,
            title=response_from_use_case.value.title,
            text=response_from_use_case.value.text,
        )

    async def resolve_save_post(self, args, context, info):
        """Сохранение нового поста."""
        request_for_use_case = NewPostRequest(request_data=args)
        repository_post = PostRepository()
        use_case_new_post = NewPostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_new_post.execute(request_object=request_for_use_case))

        if not bool(response_from_use_case):
            return False

        return PostObjectType(
            alias=response_from_use_case.value.alias,
            title=response_from_use_case.value.title,
            text=response_from_use_case.value.text,
        )


schema_blog = Schema(query=BlogQuery)
