__author__ = 'rey'

from motorengine import Document, StringField


class CatalogDocument(Document):

    __collection__ = "catalog"

    title = StringField()
    alias = StringField()