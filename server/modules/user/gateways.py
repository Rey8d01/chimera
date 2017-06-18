"""User gateways to use cases."""

import re
import transliterate
from utils.ca import RequestToUseCase
from . import domains


class SignUpRequest(RequestToUseCase):
    __slots__ = ("user", "password")

    def __init__(self, request_data: dict):
        super().__init__()

        document = request_data
        if not isinstance(request_data, dict):
            self.add_error("request_data", "Is not dict")
            document = {}

        self.user = document.get("user", "")
        self.password = document.get("password", "")


class SignInRequest(RequestToUseCase):

    __slots__ = ("user", "password")

    def __init__(self, request_data: dict):
        super().__init__()

        document = request_data
        if not isinstance(request_data, dict):
            self.add_error("request_data", "Is not dict")
            document = {}

        self.user = document.get("user", "")
        self.password = document.get("password", "")
