"""User use cases."""

from utils.ca import ErrorResponse, ResponseFromUseCase, SuccessResponse, UseCase
from utils.token import encode_token
from .gateways import SignInRequest, SignUpRequest
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

        token = encode_token(claims={"who": user.meta_info.user})
        return SuccessResponse(token)
