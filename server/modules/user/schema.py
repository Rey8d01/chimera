"""User schema GraphQL."""

import typing

from graphene import Field, ObjectType, String
from tornado.platform.asyncio import to_asyncio_future

from utils.ca import ErrorResponse, RequestToUseCase, SuccessResponse, UseCase
from utils.ql import need_auth
from utils.token import Token
from .domains import User
from .gateways import RefreshRequest, SignInRequest, SignUpRequest
from .repositories import UserRepository
from .use_cases import RefreshUseCase, SignInUseCase, SignUpUseCase


async def _simple_resolver(info, class_request: typing.Type[RequestToUseCase], class_use_case: typing.Type[UseCase], *args, **kwargs) -> SuccessResponse:
    """Типичный резолвер."""
    request = class_request(current_user=info.context.get("current_user"), **kwargs)
    repository = UserRepository(client_motor=info.context.get("client_motor"))
    use_case = class_use_case(repository)
    response = await to_asyncio_future(use_case.execute(request=request))

    if isinstance(response, ErrorResponse):
        raise Exception(str(response))
    return response


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

    async def resolve_sign_up(self, info, *args, **kwargs) -> UserObjectType:
        """Регистрация."""
        response = await _simple_resolver(info, SignUpRequest, SignUpUseCase, *args, **kwargs)
        user: User = response.data
        return UserObjectType(user.meta_info.user)

    async def resolve_sign_in(self, info, *args, **kwargs) -> TokenObjectType:
        """Авторизация."""
        response = await _simple_resolver(info, SignInRequest, SignInUseCase, *args, **kwargs)
        token: Token = response.data
        return TokenObjectType(token)

    @need_auth
    async def resolve_refresh(self, info, *args, **kwargs) -> TokenObjectType:
        """Обновление токена."""
        response = await _simple_resolver(info, RefreshRequest, RefreshUseCase, *args, **kwargs)
        token: Token = response.data
        return TokenObjectType(token)
