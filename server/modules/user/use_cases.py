"""User use cases."""

from utils.ca import ErrorResponse, ResponseFromUseCase, SuccessResponse, UseCase
from utils.token import Token
from .gateways import SignInRequest, SignUpRequest, RefreshRequest
from .repositories import UserRepository


class SignUpUseCase(UseCase):
    """Сценарий регистрации."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request_object: SignUpRequest) -> ResponseFromUseCase:
        user = await self.repository.create_user(user=request_object.user, password=request_object.password)
        if not user:
            return ErrorResponse("error create")
        return SuccessResponse(user)


class SignInUseCase(UseCase):
    """Сценарий авторизации."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request_object: SignInRequest) -> ResponseFromUseCase:
        user = await self.repository.check_user(user=request_object.user, password=request_object.password)
        if not user:
            return ErrorResponse("error user")

        token = Token(repository_user=self.repository, username=user.meta_info.user)
        return SuccessResponse(token.encode())


class RefreshUseCase(UseCase):
    """Сценарий обновления токена."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request_object: RefreshRequest) -> ResponseFromUseCase:
        token = Token(repository_user=self.repository, username=request_object.user.meta_info.user)
        return SuccessResponse(token.encode())
