"""User use cases."""

from utils.ca import ErrorResponse, ResponseFromUseCase, SuccessResponse, UseCase
from utils.token import Token
from .gateways import SignInRequest, SignUpRequest, RefreshRequest
from .repositories import UserRepository


class SignUpUseCase(UseCase):
    """Сценарий регистрации."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request: SignUpRequest) -> ResponseFromUseCase:
        user = await self.repository.create_user(user=request.user, password=request.password)
        if not user:
            return ErrorResponse("error create")
        return SuccessResponse(user)


class SignInUseCase(UseCase):
    """Сценарий авторизации."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request: SignInRequest) -> ResponseFromUseCase:
        user = await self.repository.check_user(user=request.user, password=request.password)
        if not user:
            return ErrorResponse("error user")

        token = Token(repository_user=self.repository, username=user.meta_info.user)
        return SuccessResponse(token.encode())


class RefreshUseCase(UseCase):
    """Сценарий обновления токена."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request: RefreshRequest) -> ResponseFromUseCase:
        token = Token(repository_user=self.repository, username=request.current_user.meta_info.user)
        return SuccessResponse(token.encode())
