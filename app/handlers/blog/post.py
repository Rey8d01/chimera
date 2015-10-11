"""
Обработчики записей в блоге
"""

import system.handler
import system.utils.exceptions
from tornado.gen import coroutine
from documents.blog.post import PostDocument, PostMetaDocument


class PostHandler(system.handler.MainHandler):
    @coroutine
    def get(self, alias):
        """

        :param alias:
        :return:
        """

        collection_post = yield PostDocument() \
            .objects \
            .filter({PostDocument.alias.name: alias}) \
            .find_all()

        if not collection_post:
            raise system.utils.exceptions.NotFound(error="Пост не найден")
        document_post = collection_post[0]

        raise system.utils.exceptions.Result(content=document_post.to_son())

    @coroutine
    def post(self):
        # data = self.escape.json_decode(self.request.body)
        data = self.request.arguments

        document_post = PostDocument()

        document_post.title = data[PostDocument.title.name]
        document_post.alias = data[PostDocument.alias.name]
        document_post.text = data[PostDocument.text.name]
        document_post.catalogAlias = data[PostDocument.catalogAlias.name]

        document_post_meta = PostMetaDocument()
        document_post.meta = document_post_meta

        # Теги разделяем запятыми и тримируем
        import re
        tags = re.split(',', data[PostDocument.tags.name])
        map(str.strip, tags)
        document_post.tags = tags

        yield document_post.save()

        raise system.utils.exceptions.Result(content=document_post.to_son())
