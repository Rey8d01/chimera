"""Blog schema GraphQL."""

import typing

from graphene import Boolean, Field, Int, List, ObjectType, Schema, String
from tornado.platform.asyncio import to_asyncio_future

from utils.ca import ErrorResponse, RequestToUseCase, SuccessResponse, UseCase
from utils.ql import need_auth
from .gateways import CreatePostRequest, DeletePostRequest, ItemPostRequest, ListPostsRequest, UpdatePostRequest
from .repositories import PostRepository
from .use_cases import CreatePostUseCase, DeletePostUseCase, ItemPostUseCase, ListPostsUseCase, UpdatePostUseCase


async def _simple_resolver(info, class_request: typing.Type[RequestToUseCase], class_use_case: typing.Type[UseCase], *args, **kwargs) -> SuccessResponse:
    """Типичный резолвер."""
    request = class_request(current_user=info.context.get("current_user"), **kwargs)
    repository = PostRepository(client_motor=info.context.get("client_motor"))
    use_case = class_use_case(repository)
    response = await to_asyncio_future(use_case.execute(request=request))

    if isinstance(response, ErrorResponse):
        raise Exception(str(response))
    return response


class PostObjectType(ObjectType):
    """Схема документа Post для генерации ответов."""

    # id = String()
    alias = String()
    title = String()
    text = String()


class ListPostsObjectType(ObjectType):
    """Список документов Post."""
    items = List(PostObjectType)


class BlogQuery(ObjectType):
    """Обработка запросов блога с использованием GraphQL."""

    post = Field(PostObjectType, alias=String())
    list_posts_by_tag = Field(ListPostsObjectType, alias_tag=String(), current_page=Int())
    list_posts_by_user = Field(ListPostsObjectType, user_id=String(), current_page=Int())
    create_post = Field(PostObjectType, alias=String(), title=String(), text=String())
    update_post = Field(Boolean, alias=String(), title=String(), text=String())
    delete_post = Field(Boolean, alias=String(), title=String(), text=String())

    async def resolve_post(self, info, *args, **kwargs) -> PostObjectType:
        """Запрос поста по его псевдониму."""
        response = await _simple_resolver(info, ItemPostRequest, ItemPostUseCase, *args, **kwargs)
        return PostObjectType(
            alias=response.data.alias,
            title=response.data.title,
            text=response.data.text,
        )

    async def resolve_list_posts_by_tag(self, info, *args, **kwargs) -> ListPostsObjectType:
        """Запрос на получение информации по содержимому определенного тега."""
        response = await _simple_resolver(info, ListPostsRequest, ListPostsUseCase, *args, **kwargs)
        return ListPostsObjectType(items=response.data)

    async def resolve_list_posts_by_user(self, info, *args, **kwargs) -> ListPostsObjectType:
        """Запрос на получение информации по постам от определенного автора."""
        response = await _simple_resolver(info, ListPostsRequest, ListPostsUseCase, *args, **kwargs)
        return ListPostsObjectType(items=response.data)

    @need_auth
    async def resolve_create_post(self, info, *args, **kwargs) -> PostObjectType:
        """Сохранение нового поста."""
        response = await _simple_resolver(info, CreatePostRequest, CreatePostUseCase, *args, **kwargs)
        return PostObjectType(
            alias=response.data.alias,
            title=response.data.title,
            text=response.data.text,
        )

    @need_auth
    async def resolve_update_post(self, info, *args, **kwargs) -> Boolean:
        """Обновление существующего поста."""
        response = await _simple_resolver(info, UpdatePostRequest, UpdatePostUseCase, *args, **kwargs)
        return Boolean(response.data)

    @need_auth
    async def resolve_delete_post(self, info, *args, **kwargs) -> Boolean:
        """Удаление существующего поста."""
        response = await _simple_resolver(info, DeletePostRequest, DeletePostUseCase, *args, **kwargs)
        return Boolean(response.data)


schema_blog = Schema(query=BlogQuery)
