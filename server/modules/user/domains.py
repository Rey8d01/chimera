"""Документы для хранения информации пользователей."""
import typing
from datetime import datetime

from bson.objectid import ObjectId

from utils.db import DocumentDomain


class OAuthInfo(DocumentDomain):
    """Данные по авторизации через соцсети.

    :type oauth_type: str Тип социальной сети (уникальное имя);
    :type oauth_id: str Идентификатор пользователя в социальной сети (возвращается после клиентской авторизации);
    :type name: str Имя пользователя из профиля социальной сети;
    :type alias: str Псевдоним - ник;
    :type avatar: str Урл до аватара пользователя;
    :type email: str Почтовый адрес (если социальная сеть его может отдавать);
    :type raw: str Набор информации которая была возвращена социальной сетью (в виде JSON);
    :type main: bool Параметр для главной учетки из социальной сети (необходимо для выбора типовой информации по пользователю);
    """

    __slots__ = ("oauth_type", "oauth_id", "name", "alias", "avatar", "email", "raw", "main")

    def __init__(self, oauth_type: str, oauth_id: str, name: str, alias: str, avatar: str, email: str, raw: str, main: bool, *args,
                 **kwargs):
        self.oauth_type = oauth_type
        self.oauth_id = oauth_id
        self.name = name
        self.alias = alias
        self.avatar = avatar
        self.email = email
        self.raw = raw
        self.main = main

    def to_document(self):
        return {
            "oauthType": self.oauth_type,
            "oauthId": self.oauth_id,
            "name": self.name,
            "alias": self.alias,
            "avatar": self.avatar,
            "email": self.email,
            "raw": self.raw,
            "main": self.main,
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            oauth_type=document["oauthType"],
            oauth_id=document["oauthId"],
            name=document["name"],
            alias=document["alias"],
            avatar=document["avatar"],
            email=document["email"],
            raw=document["raw"],
            main=document["main"],
        )


class DetailInfo(DocumentDomain):
    """Некие информационные поля.

    :type data: dict Неформализованная информация по пользователю;
    """

    __slots__ = ("data",)

    def __init__(self, data: dict = None, *args, **kwargs):
        self.data = data or {}

    def to_document(self):
        return {
            "data": self.data,
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            data=document["data"],
        )


class MetaInfo(DocumentDomain):
    """Всякая сервисная информация.

    :type date_registration: str Дата регистрации;
    :type date_last_activity: str Дата последнего запроса к системе;
    """

    __slots__ = ("date_registration", "date_last_activity", "login", "password", "is_active")

    def __init__(self, date_registration: datetime = None, date_last_activity: datetime = None, login: str = None, password: str = None,
                 is_active: bool = None, *args, **kwargs):
        self.date_registration = date_registration
        self.date_last_activity = date_last_activity
        self.login = login
        self.password = password
        self.is_active = is_active or True

    def to_document(self):
        return {
            "dateRegistration": self.date_registration,
            "dateLastActivity": self.date_last_activity,
            "login": self.login,
            "password": self.password,
            "isActive": self.is_active,
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            date_registration=document["dateRegistration"],
            date_last_activity=document["dateLastActivity"],
            login=document["login"],
            password=document["password"],
            is_active=document["isActive"],
        )


class User(DocumentDomain):
    """Основной документ.

    :type detail_info: DetailInfo Информация по пользователю;
    :type meta_info: MetaInfo Служебная информация;
    :type list_oauth_info: typing.List[OAuthInfo] Список идентификаций через социальные сети данного пользователя;
    # :type critic: dict Данные критики пользователя для работы нс;
    """

    __slots__ = ("_id", "detail_info", "meta_info", "list_oauth_info")

    def __init__(self, detail_info: typing.Union[DetailInfo, dict], meta_info: typing.Union[MetaInfo, dict],
                 list_oauth_info: typing.List[OAuthInfo], _id: typing.Optional[ObjectId] = None, *args, **kwargs):
        self._id = _id
        self.detail_info = DetailInfo(**detail_info) if isinstance(detail_info, dict) else detail_info
        self.meta_info = MetaInfo(**meta_info) if isinstance(meta_info, dict) else meta_info
        self.list_oauth_info = list_oauth_info or []

    def __str__(self):
        return self.meta_info.login

    def to_document(self):
        return {
            "_id": self._id,
            "detailInfo": self.detail_info.to_document(),
            "metaInfo": self.meta_info.to_document(),
            "listOauthInfo": [oauth_info.to_document() for oauth_info in self.list_oauth_info],
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            _id=document["_id"],
            detail_info=document["detailInfo"],
            meta_info=document["metaInfo"],
            list_oauth_info=document["listOauthInfo"],
        )

    # critic = BaseField()

    # def get_main_oauth_document(self) -> UserOAuthDocument:
    #     """Вернет главный документ социальной сети текущего документа пользователя."""
    #     for document_oauth in self.oauth:
    #         if document_oauth.main:
    #             return document_oauth
    #     return UserOAuthDocument()

    # def get_user_name(self) -> str:
    #     """Реализует вывод имени пользователя, в зависимости от актуальной схемы."""
    #     return self.get_main_oauth_document().name

    # @staticmethod
    # def get_list_critic(collection_user):
    #     """Формирование массива данных для анализа - массив данных имеет вид [ид_пользователя => [ид_объекта => оценка,],... ]
    #     :param collection_user:
    #     :return:
    #     """
    #     return {str(document_critic._id): document_critic.critic for document_critic in collection_user}
