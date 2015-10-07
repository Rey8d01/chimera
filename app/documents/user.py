from motorengine import Document, EmbeddedDocumentField, StringField, ListField, JsonField, DateTimeField, BaseField


class UserOAuthDocument(Document):
    """
    Данные по авторизации через соцсети
    """
    type = StringField(required=True)  # twitter
    id = StringField(required=True)  # 1234

    name = StringField()  # John Doe
    alias = StringField()  # john87
    avatar = StringField()
    email = StringField()  # john@doe.com
    raw = JsonField()


class UserInfoDocument(Document):
    """
    Некие информационные полявв
    """
    data = JsonField()


class UserMetaDocument(Document):
    """
    Всякая сервисная информация
    """
    dateRegistration = DateTimeField(auto_now_on_insert=True)
    dateLastActivity = DateTimeField()


class UserDocument(Document):
    """
    Основной документ
    """
    __collection__ = "user"

    info = EmbeddedDocumentField(UserInfoDocument)
    meta = EmbeddedDocumentField(UserMetaDocument)
    oauth = ListField(EmbeddedDocumentField(UserOAuthDocument))
    critic = BaseField()
