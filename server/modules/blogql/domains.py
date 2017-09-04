"""Blog domains.

Документы для блога.

Имеются записи, сгруппированные в иерархические каталоги и имеющие возможность проставления тегов.
В рамках блога можно просматривать отедльный каталог в рамках которого будут показаны превью постов, а так же список каталогов
относящихся к текущему каталогу.

Каталогам необходимо присваивать уникальный псевдоним, который будет использоваться в качестве сегмента урла для его идентификации.
Аналогичноя необходимость есть и у постов.

"""

from typing import List, Dict
from datetime import datetime

from modules.user.domains import User


class PostMetaInfo:
    """Класс для сбора служебной информации поста."""

    __slots__ = ("user", "date_create", "date_update")

    def __init__(self, user: User = None, date_create: datetime = None, date_update: datetime = None, *args, **kwargs):
        self.user = user
        self.date_create = date_create
        self.date_update = date_update

    def to_dict(self):
        return {
            "user": str(self.user),
            "date_create": self.date_create,
            "date_update": self.date_update,
        }


class PostTag:
    """Сущность экземпляра тега."""

    __slots__ = ("alias", "title")

    def __init__(self, alias: str, title: str, *args, **kwargs):
        self.alias = alias
        self.title = title

    def to_dict(self):
        return {
            "alias": self.alias,
            "title": self.title,
        }


class Post:
    """Документ записи в блоге (пост)."""

    __slots__ = ("alias", "title", "text", "list_tags", "meta_info")

    def __init__(self, alias: str, title: str, text: str, list_tags: List[PostTag] = None, meta_info: PostMetaInfo = None, *args, **kwargs):
        self.alias = alias
        self.title = title
        self.text = text
        self.list_tags = list_tags or []
        self.meta_info = meta_info or PostMetaInfo()

    def to_dict(self):
        return {
            "alias": self.alias,
            "title": self.title,
            "text": self.text,
            "list_tags": [tag.to_dict() for tag in self.list_tags],
            "meta_info": self.meta_info.to_dict(),
        }
