"""Набор документов для формирования поста."""

from motorengine import EmbeddedDocumentField, StringField, ListField, DateTimeField, ReferenceField

from components.document import BaseDocument
from documents.user import UserDocument


class PostTagsDocument(BaseDocument):
    """Теги для постов.

    Одиночные документы которые используется в рамках списка тегов для поиска и описания тем для поста.

    :type title: str Заголовок тега;
    :type alias: str Псевдоним тега;
    """
    title = StringField(required=True)
    alias = StringField(required=True)


class PostMetaDocument(BaseDocument):
    """Набор служебной информации о посте о датах создания/изменения поста, информация об авторе и т.д.

    :type dateCreate: str Дата создания;
    :type dateUpdate: str Дата создания;
    :type author: str Имя автора поста;
    :type user: UserDocument Документ автора поста;
    """
    user = ReferenceField(reference_document_type=UserDocument)
    author = StringField()
    dateCreate = DateTimeField(auto_now_on_insert=True)
    dateUpdate = DateTimeField(auto_now_on_update=True)


class PostDocument(BaseDocument):
    """Пост - текстовая запись.

    Относиться к каталогу, имеет сервисную информацию о себе, позволяет теггирование.

    :type alias: str Псевдоним поста для использования его в url для последующей идентификации;
    # :type catalogAlias: str Псеводним каталога к которому относится пост и который будет показываться в рамках этой категории;
    :type title: str Человеческий заголовок для поста;
    :type tags: list Список названий тегов для последующего теггирования и выбора постов по одинаковым тегам;
    :type meta: PostMetaDocument Сервисная информация о посте - дате создания, авторе, и т.д.;
    :type text: str Текст поста;
    """
    __collection__ = "post"

    alias = StringField(required=True, unique=True)
    # catalogAlias = StringField()
    title = StringField()
    tags = ListField(EmbeddedDocumentField(embedded_document_type=PostTagsDocument))
    meta = EmbeddedDocumentField(embedded_document_type=PostMetaDocument, default=PostMetaDocument())
    text = StringField()

    async def check_authorship(self, document_user: UserDocument):
        return self.meta.user == document_user._id
