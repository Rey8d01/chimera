"""Документ для сбора базовой информации на основе которой строиться система рекомендаций."""

from system.document import BaseDocument
from documents.user import UserDocument
from motorengine import StringField, IntField, ReferenceField, DateTimeField


class CriticDocument(BaseDocument):
    """Документ - критик.

    Состоит из набора информации связи объект критики (фильм) - субъект (пользователь) - оценка, а так же служебной информации.

    """
    __collection__ = "critic"

    user = ReferenceField(reference_document_type=UserDocument)
    imdb = StringField()
    rate = IntField()
    year = IntField()
    title = StringField()
    dateCreate = DateTimeField(auto_now_on_insert=True)
    dateUpdate = DateTimeField(auto_now_on_update=True)
