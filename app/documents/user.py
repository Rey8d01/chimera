"""Документы для хранения информации пользователей."""
from motorengine import Document, EmbeddedDocumentField, StringField, ListField, JsonField, DateTimeField, BaseField, BooleanField


class UserOAuthDocument(Document):
    """Данные по авторизации через соцсети.

    :type type: str Тип социальной сети (уникальное имя);
    :type id: str Идентификатор пользователя в социальной сети (возвращается после клиентской авторизации);
    :type name: str Имя пользователя из профиля социальной сети;
    :type alias: str Псевдоним - ник;
    :type avatar: str Урл до аватара пользователя;
    :type email: str Почтовый адрес (если социальная сеть его может отдавать);
    :type raw: str Набор информации которая была возвращена социальной сетью (в виде JSON);
    :type main: bool Параметр для главной учетки из социальной сети (необходимо для выбора типовой информации по пользователю);
    """
    type = StringField(required=True)
    id = StringField(required=True)
    name = StringField()
    alias = StringField()
    avatar = StringField()
    email = StringField()
    raw = JsonField()
    main = BooleanField(default=False)


class UserInfoDocument(Document):
    """Некие информационные поля.

    :type data: dict Неформализованная информация по пользователю;
    """
    data = BaseField()


class UserMetaDocument(Document):
    """Всякая сервисная информация.

    :type dateRegistration: str Дата регистрации;
    :type dateLastActivity: str Дата последнего запроса к системе;
    """
    dateRegistration = DateTimeField(auto_now_on_insert=True)
    dateLastActivity = DateTimeField()


class UserDocument(Document):
    """Основной документ.

    :type info: UserInfoDocument Информация по пользователю;
    :type meta: UserMetaDocument Служебная информация;
    :type oauth: list[UserOAuthDocument] Список идентификаций через социальные сети данного пользователя;
    :type critic: dict Данные критики пользователя для работы нс;
    """
    __collection__ = "user"

    info = EmbeddedDocumentField(UserInfoDocument)
    meta = EmbeddedDocumentField(UserMetaDocument)
    oauth = ListField(EmbeddedDocumentField(UserOAuthDocument))
    critic = BaseField()

    def get_main_oauth_document(self) -> UserOAuthDocument:
        """Вернет главный документ социальной сети текущего документа пользователя."""
        for document_oauth in self.oauth:
            if document_oauth.main:
                return document_oauth
        return UserOAuthDocument()
