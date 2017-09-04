"""Blog schema GraphQL."""

from graphene import Boolean, Field, Int, List, ObjectType, Schema, String
from tornado.platform.asyncio import to_asyncio_future

from utils.ca import ErrorResponse
from utils.ql import need_auth
from .gateways import CreatePostRequest, DeletePostRequest, ItemPostRequest, ListPostsRequest, UpdatePostRequest
from .repositories import PostRepository
from .use_cases import CreatePostUseCase, DeletePostUseCase, ItemPostUseCase, ListPostsUseCase, UpdatePostUseCase


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

    async def resolve_post(self, args, context, info) -> PostObjectType:
        """Запрос поста по его псевдониму."""
        request_item_post = ItemPostRequest(**args)
        repository_post = PostRepository(client_motor=context["client_motor"])
        use_case_item_post = ItemPostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_item_post.execute(request_object=request_item_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return PostObjectType(
            alias=response_from_use_case.data.alias,
            title=response_from_use_case.data.title,
            text=response_from_use_case.data.text,
        )

    async def resolve_list_posts_by_tag(self, args, context, info) -> ListPostsObjectType:
        """Запрос на получение информации по содержимому определенного тега."""
        request_list_posts = ListPostsRequest(**args)
        repository_post = PostRepository(client_motor=context["client_motor"])
        use_case_list_posts = ListPostsUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_list_posts.execute(request_object=request_list_posts))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return ListPostsObjectType(items=response_from_use_case.data)

    async def resolve_list_posts_by_user(self, args, context, info) -> ListPostsObjectType:
        """Запрос на получение информации по постам от определенного автора."""
        request_list_posts = ListPostsRequest(**args)
        repository_post = PostRepository(client_motor=context["client_motor"])
        use_case_list_posts = ListPostsUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_list_posts.execute(request_object=request_list_posts))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return ListPostsObjectType(items=response_from_use_case.data)

    @need_auth
    async def resolve_create_post(self, args, context, info) -> PostObjectType:
        """Сохранение нового поста."""
        request_create_post = CreatePostRequest(user=context["current_user"], **args)
        repository_post = PostRepository(client_motor=context["client_motor"])
        use_case_create_post = CreatePostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_create_post.execute(request_object=request_create_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return PostObjectType(
            alias=response_from_use_case.data.alias,
            title=response_from_use_case.data.title,
            text=response_from_use_case.data.text,
        )

    @need_auth
    async def resolve_update_post(self, args, context, info) -> Boolean:
        """Обновление существующего поста."""
        request_update_post = UpdatePostRequest(user=context["current_user"], **args)
        repository_post = PostRepository(client_motor=context["client_motor"])
        use_case_update_post = UpdatePostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_update_post.execute(request_object=request_update_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return Boolean(response_from_use_case.data)

    @need_auth
    async def resolve_delete_post(self, args, context, info) -> Boolean:
        """Удаление существующего поста."""
        request_delete_post = DeletePostRequest(user=context["current_user"], **args)
        repository_post = PostRepository(client_motor=context["client_motor"])
        use_case_delete_post = DeletePostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_delete_post.execute(request_object=request_delete_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return Boolean(response_from_use_case.data)


schema_blog = Schema(query=BlogQuery)
