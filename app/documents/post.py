__author__ = 'rey'

from system.document import BaseDocument
from motorengine import EmbeddedDocumentField, StringField, ListField, DateTimeField


class PostTagsDocument(BaseDocument):
    title = StringField()
    alias = StringField()


class PostMetaDocument(BaseDocument):
    dateCreate = DateTimeField(auto_now_on_insert=True)
    dateUpdate = DateTimeField(auto_now_on_update=True)
    author = StringField()


class PostDocument(BaseDocument):
    __collection__ = "post"

    alias = StringField()
    aliasCatalog = StringField()
    title = StringField()
    tags = ListField(EmbeddedDocumentField(PostTagsDocument))
    meta = EmbeddedDocumentField(PostMetaDocument)
    text = StringField()