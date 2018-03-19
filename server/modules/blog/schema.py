"""Blog schema GraphQL."""

import re
from datetime import datetime

import graphene
import transliterate

from modules.user.domains import User
from utils.ql import need_auth
from . import domains
from .repositories import PostRepository


class PostObjectType(graphene.ObjectType):
    """Схема документа Post для генерации ответов."""

    # id = graphene.String()
    alias = graphene.String()
    title = graphene.String()
    text = graphene.String()


class ListPostsObjectType(graphene.ObjectType):
    """Список документов Post."""
    items = graphene.List(PostObjectType)


class BlogQuery(graphene.ObjectType):
    """Обработка запросов блога с использованием GraphQL."""

    post = graphene.Field(PostObjectType, alias=graphene.String(required=True))
    list_posts_by_tag = graphene.Field(ListPostsObjectType, alias_tag=graphene.String(required=True), current_page=graphene.Int())
    list_posts_by_user = graphene.Field(ListPostsObjectType, user_id=graphene.String(required=True), current_page=graphene.Int())

    async def resolve_post(self, info, alias) -> PostObjectType:
        """Запрос поста по его псевдониму."""
        repository = PostRepository(info.context.get("client_motor"))
        post = await repository.get_item_post_by_alias(alias)
        return PostObjectType(alias=post.alias, title=post.title, text=post.text)

    async def resolve_list_posts_by_tag(self, info, alias_tag, current_page = 0) -> ListPostsObjectType:
        """Запрос на получение информации по содержимому определенного тега."""
        repository = PostRepository(info.context.get("client_motor"))
        list_posts = await repository.get_list_posts(alias_tag=alias_tag)
        return ListPostsObjectType(items=list_posts)

    async def resolve_list_posts_by_user(self, info, user_id, current_page = 0) -> ListPostsObjectType:
        """Запрос на получение информации по постам от определенного автора."""
        repository = PostRepository(info.context.get("client_motor"))
        list_posts = await repository.get_list_posts(user_id=user_id)
        return ListPostsObjectType(items=list_posts)


class PostInput(graphene.InputObjectType):
    alias: str = graphene.String(required=True)
    title: str = graphene.String(required=True)
    text: str = graphene.String(required=True)

    def build_post(self, user: User):
        # Поиск хештегов в тексте.
        raw_tags = re.findall("[^\\\]#[\w-]+", self.text)
        clear_tags = []
        for raw_tag in raw_tags:
            tag = raw_tag[raw_tag.find("#") + 1:].lower()
            alias = transliterate.slugify(tag) if transliterate.detect_language(tag) else tag
            document_tag = domains.PostTag(title=tag, alias=alias)
            clear_tags.append(document_tag)

        meta_info = domains.PostMetaInfo(
            user=user,
            datetime_create=datetime.utcnow(),
            datetime_update=datetime.utcnow(),
        )

        post = domains.Post(
            text=self.text,
            title=self.title,
            alias=self.alias,
            tags=clear_tags,
            meta_info=meta_info
        )

        return post


class CreatePost(graphene.Mutation):
    """Создание нового поста."""

    class Arguments:
        post_input = PostInput(required=True)

    post = graphene.Field(PostObjectType)

    @need_auth
    async def mutate(self, info, post_input: PostInput = None):
        repository = PostRepository(info.context.get("client_motor"))
        user = info.context.get("current_user")
        post = await repository.create_post(post_input.build_post(user))
        if not post:
            raise Exception("Ошибка при создании поста.")

        return CreatePost(post=PostObjectType(alias=post.alias, title=post.title, text=post.text))


class UpdatePost(graphene.Mutation):
    """Изменение существующего поста."""

    class Arguments:
        post_input = PostInput(required=True)

    result = graphene.Boolean()

    @need_auth
    async def mutate(self, info, post_input: PostInput = None):
        repository = PostRepository(info.context.get("client_motor"))
        user = info.context.get("current_user")
        result = await repository.update_post(post_input.build_post(user))
        return UpdatePost(result=result)


class DeletePost(graphene.Mutation):
    """Удаление существующего поста."""

    class Arguments:
        alias = graphene.String(required=True)

    result = graphene.Boolean()

    @need_auth
    async def mutate(self, info, alias: str = None):
        repository = PostRepository(info.context.get("client_motor"))
        user = info.context.get("current_user")
        result = await repository.delete_post(alias, user)
        return DeletePost(result=result)


class BlogMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
