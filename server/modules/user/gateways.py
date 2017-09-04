"""User gateways to use cases."""

from utils.ca import RequestToUseCase


class SignUpRequest(RequestToUseCase):
    """Схема запроса для регистрации пользователя."""

    __slots__ = ("user", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        document = kwargs
        if not isinstance(document, dict):
            self.add_error("request_data", "Is not dict")
            document = {}

        self.user = document.get("user", "")
        self.password = document.get("password", "")


class SignInRequest(RequestToUseCase):
    """Схема запроса для авторизации пользователя."""

    __slots__ = ("user", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        document = kwargs
        if not isinstance(document, dict):
            self.add_error("request_data", "Is not dict")
            document = {}

        self.user = document.get("user", "")
        self.password = document.get("password", "")
