"""Blog gateways to use cases."""

import re
from datetime import datetime

import transliterate

from modules.user.domains import User
from utils.ca import RequestToUseCase
from . import domains


class ItemPostRequest(RequestToUseCase):
    """Класс запросов на получение одного поста."""

    filters = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters = kwargs

        if not isinstance(self.filters, dict):
            self.add_error("request_data", "Is not dict")


class ListPostsRequest(RequestToUseCase):
    """Класс запросов на получение списка постов."""

    filters = None

    def __init__(self, *args, **kwargs):
        # Номер страницы в списке постов. # id пользователя в базе. # Имя псевдонима тега.
        super().__init__(*args, **kwargs)

        self.filters = kwargs

        if not isinstance(self.filters, dict):
            self.add_error("request_data", "Is not dict")


class CreatePostRequest(RequestToUseCase):
    """Класс запросов на создание нового поста."""

    __slots__ = ("alias", "title", "text", "user",)

    def __init__(self, alias: str, title: str, text: str, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.alias = alias
        self.title = title
        self.text = text
        self.user = user

    def to_post(self) -> domains.Post:
        """Приведение запроса к модели поста."""
        # Поиск хештегов в тексте.
        raw_tags = re.findall("[^\\\]#[\w-]+", self.text)
        list_tags = []
        for raw_tag in raw_tags:
            tag = raw_tag[raw_tag.find("#") + 1:].lower()
            alias = transliterate.slugify(tag) if transliterate.detect_language(tag) else tag
            document_tag = domains.PostTag(title=tag, alias=alias)
            list_tags.append(document_tag)

        meta_info = domains.PostMetaInfo(
            user=self.user,
            date_create=datetime.utcnow(),
            date_update=datetime.utcnow(),
        )

        post = domains.Post(
            text=self.text,
            title=self.title,
            alias=self.alias,
            list_tags=list_tags,
            meta_info=meta_info
        )

        return post


class UpdatePostRequest(CreatePostRequest):
    """Класс запросов на обновление нового поста."""


class DeletePostRequest(RequestToUseCase):
    """Класс запросов на удаление поста."""

    __slots__ = ("alias", "user")

    def __init__(self, alias: str, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.alias = alias
        self.user = user
