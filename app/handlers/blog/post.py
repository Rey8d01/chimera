"""Обработчики записей в блоге.

Организуют доступ для чтения и записи постов в каталогах.
Посты идентифицируются по их псевдонимам, по ним очуществляется просмотр и редактирование.

"""
import system.handler
import system.utils.exceptions
from documents.blog.post import PostDocument, PostTagsDocument
import transliterate


class PostEditHandler(system.handler.BaseHandler):
    """Обработчик запросов для создания/редактирования информации по постам.

    POST - Создание нового поста возможно при отсутствии заданного псевдонима в базе данных.
    PUT - Редактирование нового поста по заданному и существующему псевдониму в базе данных.

    """

    async def post(self):
        """Создание нового поста и занесение в базу актуальной по нему информации."""
        document_post = PostDocument()
        document_post.fill_document_from_dict(self.get_bytes_body_source())

        document_user = await self.get_data_current_user()
        document_post.meta.author = document_user.get_main_oauth_document().name
        document_post.meta.user = document_user
        # Пасринг тегов - предполагается что они идут пачкой под одной переменной.
        tags = self.get_bytes_body_argument(PostDocument.tags.name)

        document_post.tags = []
        if len(tags):
            for tag in tags:
                alias = tag[PostTagsDocument.alias.name]
                alias = transliterate.slugify(alias) if transliterate.detect_language(alias) else alias
                document_tag = PostTagsDocument(title=tag[PostTagsDocument.title.name], alias=alias)
                document_post.tags.append(document_tag)

        await document_post.save()

        raise system.utils.exceptions.Result(content=document_post.to_son())

    async def put(self):
        """Изменение существующего поста."""
        alias = self.get_argument(PostDocument.alias.name)

        # Выбор поста с указанным псевдонимом (иначе исключение).
        collection_post = await PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias}) \
            .limit(1) \
            .find_all()
        if not collection_post:
            raise system.utils.exceptions.NotFound(error_message="Запись не найдена")

        document_post = collection_post[-1]
        document_post.fill_document_from_dict(self.request.arguments)
        await document_post.save()

        raise system.utils.exceptions.Result(content=document_post.to_son())


class PostHandler(system.handler.BaseHandler):
    """Обработчик запросов для указанного поста.

    GET - Запрос информации по заданному псевдониму.

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
            raise system.utils.exceptions.NotFound(error_message="Пост не найден")
        document_post = collection_post[-1]

        raise system.utils.exceptions.Result(content=document_post.to_son())
