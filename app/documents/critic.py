from motorengine import Document, StringField, IntField, ReferenceField, DateTimeField
from documents.user import UserDocument


class CriticDocument(Document):
    __collection__ = "critic"

    user = ReferenceField(reference_document_type=UserDocument)
    imdb = StringField()
    rate = IntField()
    year = IntField()
    title = StringField()

    dateCreate = DateTimeField(auto_now_on_insert=True)
    dateUpdate = DateTimeField(auto_now_on_update=True)