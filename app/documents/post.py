__author__ = 'rey'

from system.document import BaseDocument
from motorengine import EmbeddedDocumentField, StringField, ListField, DateTimeField


class PostTagsDocument(BaseDocument):
    """
    Теги для постов

    """
    title = StringField()
    alias = StringField()


class PostMetaDocument(BaseDocument):
    """
    Набор служебной информации о посте

    """
    dateCreate = DateTimeField(auto_now_on_insert=True)
    dateUpdate = DateTimeField(auto_now_on_update=True)
    author = StringField()


class PostDocument(BaseDocument):
    """
    Пост - текстовый материал. Относиться к каталогу, имеет сервисную информацию о себе, позволяет теггирование.

    :type alias: Псевдоним поста для использования его в url для последующей идентификации
    :type aliasCatalog: Псеводним каталога к которому относится пост и который будет показываться в рамках этой категории
    :type title: Человеческий заголовок для поста
    :type tags: Список названий тегов для последующего теггирования и выбора постов по одинаковым тегам
    :type meta: Сервсисная информация о посте - дате создания, авторе, и т.д.
    :type text: Текст поста
    """

    __collection__ = "post"

    alias = StringField()
    aliasCatalog = StringField()
    title = StringField()
    tags = ListField(EmbeddedDocumentField(StringField))
    meta = EmbeddedDocumentField(PostMetaDocument)
    text = StringField()