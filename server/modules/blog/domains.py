"""Blog domains.

Документы для блога.

Имеются записи, сгруппированные в иерархические каталоги и имеющие возможность проставления тегов.
В рамках блога можно просматривать отедльный каталог в рамках которого будут показаны превью постов, а так же список каталогов
относящихся к текущему каталогу.

Каталогам необходимо присваивать уникальный псевдоним, который будет использоваться в качестве сегмента урла для его идентификации.
Аналогичноя необходимость есть и у постов.

"""
import typing
from datetime import datetime

from bson.dbref import DBRef
from bson.objectid import ObjectId

from modules.user.domains import User
from utils.db import DocumentDomain


class PostMetaInfo(DocumentDomain):
    """Класс для сбора служебной информации поста."""

    __slots__ = ("user", "datetime_create", "datetime_update")

    def __init__(self, user: User = None, datetime_create: datetime = None, datetime_update: datetime = None, *args, **kwargs):
        self.user = user
        self.datetime_create = datetime_create
        self.datetime_update = datetime_update

    def to_document(self):
        return {
            "user": DBRef(collection="user", id=self.user._id),
            "datetimeCreate": self.datetime_create,
            "datetimeUpdate": self.datetime_update,
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            user=document["user"],
            datetime_create=document["datetimeCreate"],
            datetime_update=document["datetimeUpdate"],
        )


class PostTag(DocumentDomain):
    """Сущность экземпляра тега."""

    __slots__ = ("alias", "title")

    def __init__(self, alias: str, title: str, *args, **kwargs):
        self.alias = alias
        self.title = title

    def to_document(self):
        return {
            "alias": self.alias,
            "title": self.title,
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            alias=document["alias"],
            title=document["title"],
        )


class Post(DocumentDomain):
    """Документ записи в блоге (пост)."""

    __slots__ = ("alias", "title", "text", "tags", "meta_info")

    def __init__(self, alias: str, title: str, text: str, tags: typing.List[PostTag] = None, meta_info: PostMetaInfo = None,
                 _id: typing.Optional[ObjectId] = None, *args, **kwargs):
        self._id = _id
        self.alias = alias
        self.title = title
        self.text = text
        self.tags = tags or []
        self.meta_info = meta_info or PostMetaInfo()

    def to_document(self):
        return {
            "alias": self.alias,
            "title": self.title,
            "text": self.text,
            "tags": tuple(tag.to_document() for tag in self.tags),
            "metaInfo": self.meta_info.to_document(),
        }

    @classmethod
    def from_document(cls, document):
        return cls(
            _id=document["_id"],
            alias=document["alias"],
            text=document["text"],
            title=document["title"],
            tags=document["tags"],
            meta_info=document["metaInfo"],
        )
