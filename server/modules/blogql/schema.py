"""Blog schema GraphQL."""

from typing import Union
from graphene import Schema, ObjectType, Field, String, Int, List, resolve_only_args
from tornado.platform.asyncio import to_asyncio_future
from .gateways import ItemPostRequest, CreatePostRequest, UpdatePostRequest, ListPostsRequest
from .use_cases import ItemPostUseCase, CreatePostUseCase, UpdatePostUseCase, ListPostsUseCase
from .repositories import PostRepository

from utils.ca import ErrorResponse
from asyncio import coroutine, Future


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


class ListPostsObjectType(ObjectType):
    items = List(PostObjectType)


class BlogQuery(ObjectType):
    """Обработка запросов блога с использованием GraphQL."""

    post = Field(PostObjectType, alias=String())
    list_posts_by_tag = Field(ListPostsObjectType, alias_tag=String(), current_page=Int())
    list_posts_by_user = Field(ListPostsObjectType, user_id=String(), current_page=Int())
    create_post = Field(PostObjectType, alias=String(), title=String(), text=String())

    @resolve_only_args
    async def resolve_post(self, alias: str) -> Union[PostObjectType, bool]:
        """Запрос поста по его псевдониму."""
        request_item_post = ItemPostRequest(request_data={"alias": alias})
        repository_post = PostRepository()
        use_case_item_post = ItemPostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_item_post.execute(request_object=request_item_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return PostObjectType(
            alias=response_from_use_case.data.alias,
            title=response_from_use_case.data.title,
            text=response_from_use_case.data.text,
        )

    @resolve_only_args
    async def resolve_list_posts_by_tag(self, alias_tag: str, current_page: int) -> Union[ListPostsObjectType, bool]:
        """
        Запрос на получение информации по содержимому определенного тега;

        :param alias_tag: Имя псевдонима тега;
        :param current_page: Номер страницы в списке постов;
        :return: 
        """

        request_data = {
            "alias_tag": alias_tag,
            "current_page": current_page
        }
        request_list_posts = ListPostsRequest(request_data=request_data)
        repository_post = PostRepository()
        use_case_list_posts = ListPostsUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_list_posts.execute(request_object=request_list_posts))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return ListPostsObjectType(items=response_from_use_case.data)

    @resolve_only_args
    async def resolve_list_posts_by_user(self, user_id: str, current_page: int) -> Union[ListPostsObjectType, bool]:
        """
        Запрос на получение информации по постам от определенного автора;

        :param user_id: id пользователя в базе;
        :param current_page: Номер страницы в списке постов;
        :return: 
        """

        request_data = {
            "user_id": user_id,
            "current_page": current_page
        }
        request_list_posts = ListPostsRequest(request_data=request_data)
        repository_post = PostRepository()
        use_case_list_posts = ListPostsUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_list_posts.execute(request_object=request_list_posts))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return ListPostsObjectType(items=response_from_use_case.data)

    async def resolve_create_post(self, args, context, info) -> Union[PostObjectType, bool]:
        """Сохранение нового поста."""
        request_create_post = CreatePostRequest(request_data=args)
        repository_post = PostRepository()
        use_case_create_post = CreatePostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_create_post.execute(request_object=request_create_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return PostObjectType(
            alias=response_from_use_case.data.alias,
            title=response_from_use_case.data.title,
            text=response_from_use_case.data.text,
        )

    async def resolve_update_post(self, args, context, info) -> Union[PostObjectType, bool]:
        """Обновление существующего поста."""
        request_update_post = UpdatePostRequest(request_data=args)
        repository_post = PostRepository()
        use_case_update_post = UpdatePostUseCase(repository_post)
        response_from_use_case = await to_asyncio_future(use_case_update_post.execute(request_object=request_update_post))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        return PostObjectType(
            alias=response_from_use_case.value.alias,
            title=response_from_use_case.value.title,
            text=response_from_use_case.value.text,
        )

    async def resolve_delete_post(self, args, context, info) -> Union[PostObjectType, bool]:
        """Удаление существующего поста."""
        # request_for_use_case = UpdatePostRequest(request_data=args)
        # repository_post = PostRepository()
        # use_case_update_post = UpdatePostUseCase(repository_post)
        # response_from_use_case = await to_asyncio_future(use_case_update_post.execute(request_object=request_for_use_case))
        #
        # if not bool(response_from_use_case):
        #     return False
        #
        # return PostObjectType(
        #     alias=response_from_use_case.value.alias,
        #     title=response_from_use_case.value.title,
        #     text=response_from_use_case.value.text,
        # )


schema_blog = Schema(query=BlogQuery)
