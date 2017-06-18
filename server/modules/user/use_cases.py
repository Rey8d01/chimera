"""User use cases."""

from utils.ca import UseCase, SuccessResponse, ErrorResponse, ResponseFromUseCase
from .gateways import SignUpRequest, SignInRequest
from .repositories import UserRepository


class SignUpUseCase(UseCase):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request_object: SignUpRequest) -> ResponseFromUseCase:
        user = await self.repository.create_user(user=request_object.user, password=request_object.password)
        if not user:
            return ErrorResponse("error create")
        return SuccessResponse(user)


class SignInUseCase(UseCase):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def process_request(self, request_object: SignInRequest) -> ResponseFromUseCase:
        user = await self.repository.check_user(user=request_object.user, password=request_object.password)
        if not user:
            return ErrorResponse("error user")
        return SuccessResponse(user)
