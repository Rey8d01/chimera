"""Документы для хранения информации пользователей."""

from motorengine import Document, EmbeddedDocumentField, StringField, ListField, JsonField, DateTimeField, BaseField


class UserOAuthDocument(Document):
    """Данные по авторизации через соцсети."""
    type = StringField(required=True)
    id = StringField(required=True)

    name = StringField()
    alias = StringField()
    avatar = StringField()
    email = StringField()
    raw = JsonField()


class UserInfoDocument(Document):
    """Некие информационные поля."""
    data = JsonField()


class UserMetaDocument(Document):
    """Всякая сервисная информация."""
    dateRegistration = DateTimeField(auto_now_on_insert=True)
    dateLastActivity = DateTimeField()


class UserDocument(Document):
    """Основной документ."""
    __collection__ = "user"

    info = EmbeddedDocumentField(UserInfoDocument)
    meta = EmbeddedDocumentField(UserMetaDocument)
    oauth = ListField(EmbeddedDocumentField(UserOAuthDocument))
    critic = BaseField()
