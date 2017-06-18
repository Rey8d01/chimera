"""User schema GraphQL."""

from graphene import Schema, ObjectType, Field, String, Int, List, Boolean, resolve_only_args
from tornado.platform.asyncio import to_asyncio_future
from utils.ca import ErrorResponse
from .gateways import SignUpRequest, SignInRequest
from .use_cases import SignUpUseCase, SignInUseCase
from .repositories import UserRepository
from .domains import User


class UserObjectType(ObjectType):
    """Схема документа User."""

    alias = String()


class UserQuery(ObjectType):
    """Обработка запросов о пользователях."""

    sign_up = Field(UserObjectType, user=String(), password=String())
    sign_in = Field(UserObjectType, user=String(), password=String())

    async def resolve_sign_up(self, args, context, info) -> UserObjectType:
        """Регистрация."""
        request_sign_up = SignUpRequest(request_data=args)
        repository_user = UserRepository()
        use_case_sign_up = SignUpUseCase(repository_user)
        response_from_use_case = await to_asyncio_future(use_case_sign_up.execute(request_object=request_sign_up))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        user = response_from_use_case.data  # type: User
        return UserObjectType(user.meta_info.user)

    async def resolve_sign_in(self, args, context, info) -> UserObjectType:
        """Авторизация."""
        request_sign_in = SignInRequest(request_data=args)
        repository_user = UserRepository()
        use_case_sign_in = SignInUseCase(repository_user)
        response_from_use_case = await to_asyncio_future(use_case_sign_in.execute(request_object=request_sign_in))

        if isinstance(response_from_use_case, ErrorResponse):
            raise Exception(str(response_from_use_case))

        user = response_from_use_case.data  # type: User
        return UserObjectType(user.meta_info.user)
