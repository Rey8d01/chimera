"""Обработчики записей в блоге.

Организуют доступ для чтения и записи постов в каталогах.
Посты идентифицируются по их псевдонимам, по ним очуществляется просмотр и редактирование.

"""
import system.handler
import system.utils.exceptions
from tornado.gen import coroutine
from documents.blog.post import PostDocument, PostTagsDocument
from transliterate import slugify


class PostEditHandler(system.handler.BaseHandler):
    """Обработчик запросов для создания/редактирования информации по постам.

    POST - Создание нового поста возможно при отсутствии заданного псевдонима в базе данных.
    PUT - Редактирование нового поста по заданному и существующему псевдониму в базе данных.

    """

    @coroutine
    def post(self):
        """Создание нового поста и занесение в базу актуальной по нему информации."""
        document_post = PostDocument()
        document_post.fill_document_from_dict(self.request.arguments)
        # todo заменить на реального автора.
        document_post.meta.author = 'test'
        # Пасринг тегов - предполагается что они идут пачкой под одной переменной.
        tags = self.get_arguments(PostDocument.tags.name)
        if len(tags):
            document_post.tags = [PostTagsDocument(title=tag, alias=slugify(tag)) for tag in tags]

        yield document_post.save()

        raise system.utils.exceptions.Result(content=document_post.to_son())

    @coroutine
    def put(self):
        """Изменение существующего поста."""
        alias = self.get_argument(PostDocument.alias.name)

        # Выбор поста с указанным псевдонимом (иначе исключение).
        collection_post = yield PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias}) \
            .limit(1) \
            .find_all()
        if not collection_post:
            raise system.utils.exceptions.NotFound(error="Запись не найдена")

        document_post = collection_post[-1]
        document_post.fill_document_from_dict(self.request.arguments)
        yield document_post.save()

        raise system.utils.exceptions.Result(content=document_post.to_son())


class PostHandler(system.handler.BaseHandler):
    """Обработчик запросов для указанного поста.

    GET - Запрос информации по заданному псевдониму.

    """

    @coroutine
    def get(self, alias):
        """Запрос на получение информации определенного поста.

        :param alias: Имя псевдонима поста;
        :type alias: str
        """
        collection_post = yield PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias}) \
            .find_all()

        if not collection_post:
            raise system.utils.exceptions.NotFound(error="Пост не найден")
        document_post = collection_post[-1]

        raise system.utils.exceptions.Result(content=document_post.to_son())
