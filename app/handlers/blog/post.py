from tornado.gen import coroutine

import system.handler
from documents.blog.post import PostDocument, PostMetaDocument
from system.utils.exceptions import ChimeraHTTPError


class PostHandler(system.handler.BaseHandler):

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
            raise ChimeraHTTPError(404, error_message=u"Пост не найден")
        document_post = collection_post[0]

        self.result.update_content(document_post.to_son())
        self.write(self.result.get_message())

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

        self.result.update_content(document_post.to_son())
        self.write(self.result.get_message())
