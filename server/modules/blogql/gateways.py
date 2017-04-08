"""Blog gateways to use cases."""

from utils.ca import RequestToUseCase


class PostItemRequest(RequestToUseCase):
    """Класс для формализации запросов на получение одного поста."""

    filters = None

    def __init__(self, request_data: dict):
        super().__init__()

        self.filters = request_data

        if not isinstance(request_data, dict):
            self.add_error("args_query", "Is not dict")


class NewPostRequest(RequestToUseCase):
    """Класс для формализации запросов на создание нового поста."""

    doc = None

    def __init__(self, request_data: dict):
        super().__init__()

        self.doc = request_data

        if not isinstance(request_data, dict):
            self.add_error("args_query", "Is not dict")
