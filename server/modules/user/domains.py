"""Документы для хранения информации пользователей."""
from typing import List, Dict, Union
from datetime import datetime


class OAuthInfo:
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

    def __init__(self, oauth_type: str, oauth_id: str, name: str, alias: str, avatar: str, email: str, raw: str, main: bool, *args, **kwargs):
        self.oauth_type = oauth_type
        self.oauth_id = oauth_id
        self.name = name
        self.alias = alias
        self.avatar = avatar
        self.email = email
        self.raw = raw
        self.main = main

    def to_dict(self):
        return {
            "oauth_type": self.oauth_type,
            "oauth_id": self.oauth_id,
            "name": self.name,
            "alias": self.alias,
            "avatar": self.avatar,
            "email": self.email,
            "raw": self.raw,
            "main": self.main,
        }


class DetailInfo:
    """Некие информационные поля.

    :type data: dict Неформализованная информация по пользователю;
    """

    __slots__ = ("data", )

    def __init__(self, data: dict = None, *args, **kwargs):
        self.data = data or {}

    def to_dict(self):
        return {
            "data": self.data,
        }


class MetaInfo:
    """Всякая сервисная информация.

    :type date_registration: str Дата регистрации;
    :type date_last_activity: str Дата последнего запроса к системе;
    """

    __slots__ = ("date_registration", "date_last_activity", "user", "password", "is_active")

    def __init__(self, date_registration: datetime = None, date_last_activity: datetime = None, user: str = None, password: str = None, is_active: bool = None, *args, **kwargs):
        self.date_registration = date_registration
        self.date_last_activity = date_last_activity
        self.user = user
        self.password = password
        self.is_active = is_active or True

    def to_dict(self):
        return {
            "date_registration": self.date_registration,
            "date_last_activity": self.date_last_activity,
            "user": self.user,
            "password": self.password,
            "is_active": self.is_active,
        }


class User:
    """Основной документ.

    :type detail_info: DetailInfo Информация по пользователю;
    :type meta_info: MetaInfo Служебная информация;
    :type list_oauth_info: List[OAuthInfo] Список идентификаций через социальные сети данного пользователя;
    # :type critic: dict Данные критики пользователя для работы нс;
    """

    __slots__ = ("detail_info", "meta_info", "list_oauth_info")

    def __init__(self, detail_info: Union[DetailInfo, dict], meta_info: Union[MetaInfo, dict], list_oauth_info: List[OAuthInfo], *args, **kwargs):
        self.detail_info = DetailInfo(**detail_info) if isinstance(detail_info, dict) else detail_info
        self.meta_info = MetaInfo(**meta_info) if isinstance(meta_info, dict) else meta_info
        self.list_oauth_info = list_oauth_info or []

    def to_dict(self):
        return {
            "detail_info": self.detail_info.to_dict(),
            "meta_info": self.meta_info.to_dict(),
            "list_oauth_info": [oauth_info.to_dict() for oauth_info in self.list_oauth_info],
        }

    def __str__(self):
        return self.meta_info.user

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
