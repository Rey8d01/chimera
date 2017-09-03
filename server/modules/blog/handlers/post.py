"""Обработчики записей в блоге.

Организуют доступ для чтения и записи постов в каталогах.
Посты идентифицируются по их псевдонимам, по ним осуществляется просмотр и редактирование.

"""
import re

import transliterate

import modules.handler
import utils.exceptions
from modules.blog.documents.post import PostDocument, PostTagsDocument, PostMetaDocument
from utils.pagination import Pagination


class PostItemHandler(modules.handler.MainHandler):
    """Обработчик запросов для редактирования информации по постам.

    POST - Создание нового поста возможно при отсутствии заданного псевдонима в базе данных.
    PUT - Редактирование нового поста по заданному и существующему псевдониму в базе данных.
    DELETE - Удаление поста по заданному и существующему псевдониму в базе данных.

    """

    async def get(self, alias: str):
        """Запрос на получение информации определенного поста.

        :param alias: Имя псевдонима поста;
        """
        collection_post = await PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias}) \
            .find_all()

        if not collection_post:
            raise utils.exceptions.NotFound(error_message="Пост не найден")
        document_post = collection_post[-1]

        raise utils.exceptions.Result(content=document_post.to_json())

    async def post(self):
        """Создание нового поста и занесение в базу актуальной по нему информации."""
        document_post = PostDocument()
        document_post.fill_document_from_dict(self.get_bytes_body_source())

        document_user = self.current_user
        document_post.meta.author = document_user.get_main_oauth_document().name
        document_post.meta.user = document_user

        # Поиск хештегов в тексте.
        raw_tags = re.findall("[^\\\]#[\w-]+", document_post.text)
        document_post.tags = []
        for raw_tag in raw_tags:
            tag = raw_tag[raw_tag.find("#") + 1:].lower()
            alias = transliterate.slugify(tag) if transliterate.detect_language(tag) else tag
            document_tag = PostTagsDocument(title=tag, alias=alias)
            document_post.tags.append(document_tag)

        await document_post.save()

        raise utils.exceptions.Result(content=document_post.to_json())

    async def put(self):
        """Изменение существующего поста."""
        alias = self.get_argument(PostDocument.alias.name)
        document_user = self.current_user

        # Выбор поста с указанным псевдонимом (иначе исключение).
        collection_post = await PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias, PostDocument.meta.name + "." + PostMetaDocument.user.name: str(document_user._id)}) \
            .limit(1) \
            .find_all()
        if not collection_post:
            raise utils.exceptions.NotFound(error_message="Запись не найдена")
        document_post = collection_post[-1]

        document_post.fill_document_from_dict(self.request.arguments)
        await document_post.save()

        raise utils.exceptions.Result(content=document_post.to_json())

    async def delete(self, alias: str):
        """Удаление существующего поста."""
        document_user = self.current_user

        # Выбор поста с указанным псевдонимом (иначе исключение).
        collection_post = await PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias, PostDocument.meta.name + "." + PostMetaDocument.user.name: str(document_user._id)}) \
            .find_all()
        if not collection_post:
            raise utils.exceptions.NotFound(error_message="Запись не найдена")
        document_post = collection_post[-1]

        await document_post.delete()

        raise utils.exceptions.Result()


class PostListHandler(modules.handler.BaseHandler):
    """Обработчик запросов для указанного каталога.

    GET - Запрос информации по заданному псевдониму (с постраничной навигацией).
    """

    async def get(self, type_list: str, current_page: int):
        """Запрос на получение информации по содержимому определенного каталога.

        :param type_list: todo;
        :param current_page: Номер страницы в списке постов;
        """
        current_page = int(current_page)
        result = {}

        # Для особых псевдонимов генерируем свой набор данных.
        count_post = await PostDocument().objects.count()
        pagination = Pagination(count_post, current_page, 5)

        collection_post = await PostDocument() \
            .objects \
            .sort(PostDocument.meta.name + "." + PostMetaDocument.dateCreate.name, direction=1) \
            .limit(pagination.count_items_on_page) \
            .skip(pagination.skip_items) \
            .find_all()

        list_items_post = []
        for document_post in collection_post:
            pattern = re.compile(r'<.*?>')
            clear_text = pattern.sub('', document_post.text)
            clipped_text = re.split('\s+', clear_text)[:10]

            document_post.text = " ".join(clipped_text)

            list_items_post.append(document_post.to_json())

        result.update({
            "posts": list_items_post,
            "pageData": {
                "currentPage": pagination.current_page,
                "pageSize": pagination.count_items_on_page,
                "total": pagination.count_all_items,
            }
        })

        raise utils.exceptions.Result(content=result)
