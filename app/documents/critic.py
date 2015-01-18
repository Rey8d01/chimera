__author__ = 'rey'

from motorengine import Document, StringField, IntField, ReferenceField
from documents.user import UserDocument


class CriticDocument(Document):
    __collection__ = "critic"

    user = ReferenceField(reference_document_type=UserDocument)
    imdb = StringField()
    rate = IntField()
    year = IntField()
    title = StringField()