"""Blog gateways to use cases."""

import re
import transliterate
from utils.ca import RequestToUseCase
from . import domains


class ItemPostRequest(RequestToUseCase):
    """Класс запросов на получение одного поста."""

    filters = None

    def __init__(self, request_data: dict):
        super().__init__()

        self.filters = request_data

        if not isinstance(request_data, dict):
            self.add_error("request_data", "Is not dict")


class ListPostsRequest(RequestToUseCase):
    """Класс запросов на получение списка постов."""

    filters = None

    def __init__(self, request_data: dict):
        super().__init__()

        self.filters = request_data

        if not isinstance(request_data, dict):
            self.add_error("request_data", "Is not dict")


class CreatePostRequest(RequestToUseCase):
    """Класс запросов на создание нового поста."""

    __slots__ = ("alias", "title", "text", "user",)

    def __init__(self, request_data: dict):
        super().__init__()

        document = request_data
        if not isinstance(request_data, dict):
            self.add_error("request_data", "Is not dict")
            document = {}

        self.alias = document.get("alias", "")
        self.title = document.get("title", "")
        self.text = document.get("text", "")
        # self.user = document.get("user", "")

    def to_post(self):
        # Поиск хештегов в тексте.
        raw_tags = re.findall("[^\\\]#[\w-]+", self.text)
        list_tags = []
        for raw_tag in raw_tags:
            tag = raw_tag[raw_tag.find("#") + 1:].lower()
            alias = transliterate.slugify(tag) if transliterate.detect_language(tag) else tag
            document_tag = domains.PostTag(title=tag, alias=alias)
            list_tags.append(document_tag)

        # meta_info = domains.PostMetaInfo(user=self.user)
        post = domains.Post(
            text=self.text,
            title=self.title,
            alias=self.alias,
            list_tags=list_tags,
            # meta_info=meta_info
        )

        return post


class UpdatePostRequest(CreatePostRequest):
    """Класс запросов на обновление нового поста."""


class DeletePostRequest(RequestToUseCase):
    """Класс запросов на удаление поста."""

    __slots__ = ("alias", )

    def __init__(self, request_data: dict):
        super().__init__()

        document = request_data
        if not isinstance(request_data, dict):
            self.add_error("request_data", "Is not dict")
            document = {}

        self.alias = document.get("alias", "")
