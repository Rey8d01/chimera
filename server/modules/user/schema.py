"""User schema GraphQL."""

from graphene import Field, ObjectType, String
from tornado.platform.asyncio import to_asyncio_future

from utils.ca import ErrorResponse
from .domains import User
from .gateways import SignInRequest, SignUpRequest, RefreshRequest
from .repositories import UserRepository
from .use_cases import SignInUseCase, SignUpUseCase, RefreshUseCase
from utils.ql import need_auth
from utils.token import Token


class UserObjectType(ObjectType):
    """Схема документа User."""

    alias = String()


class TokenObjectType(ObjectType):
    """Схема токена."""

    token = String()


class UserQuery(ObjectType):
    """Обработка запросов о пользователях."""

    sign_up = Field(UserObjectType, user=String(), password=String())
    sign_in = Field(TokenObjectType, user=String(), password=String())
    refresh = Field(TokenObjectType)

    async def resolve_sign_up(self, args, context, info) -> UserObjectType:
        """Регистрация."""
        request_sign_up = SignUpRequest(**args)
        repository_user = UserRepository(client_motor=context["client_motor"])
        use_case_sign_up = SignUpUseCase(repository_user)
        response_from_use_case = await to_asyncio_future(use_case_sign_up.execute(request_object=request_sign_up))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        user: User = response_from_use_case.data
        return UserObjectType(user.meta_info.user)

    async def resolve_sign_in(self, args, context, info) -> TokenObjectType:
        """Авторизация."""
        request_sign_in = SignInRequest(**args)
        repository_user = UserRepository(client_motor=context["client_motor"])
        use_case_sign_in = SignInUseCase(repository_user)
        response_from_use_case = await to_asyncio_future(use_case_sign_in.execute(request_object=request_sign_in))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        token: Token = response_from_use_case.data
        return TokenObjectType(token)

    @need_auth
    async def resolve_refresh(self, args, context, info) -> TokenObjectType:
        """Обновление токена."""
        request_sign_in = RefreshRequest(user=context["current_user"], **args)
        repository_user = UserRepository(client_motor=context["client_motor"])
        use_case_refresh = RefreshUseCase(repository_user)
        response_from_use_case = await to_asyncio_future(use_case_refresh.execute(request_object=request_sign_in))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        token: Token = response_from_use_case.data
        return TokenObjectType(token)
