"""Схема запросов пользовательской информации."""
import graphene
from graphene.types.inputobjecttype import InputObjectType

from utils.ql import need_auth
from utils.token import Token
from .domains import User
from .repositories import UserRepository


class UserObjectType(graphene.ObjectType):
    """Схема документа User."""
    alias = graphene.String()


class UserQuery(graphene.ObjectType):
    """Обработка запросов о пользователях."""
    # not use


class UserPasswordInput(InputObjectType):
    login = graphene.String(required=True)
    password = graphene.String(required=True)


class SignUp(graphene.Mutation):
    """Регистрация."""

    class Arguments:
        user_password_input = UserPasswordInput(required=True)

    user = graphene.Field(UserObjectType)

    async def mutate(self, info, user_password_input: UserPasswordInput):
        repository = UserRepository(info.context.get("client_motor"))
        user = await repository.create_user(login=user_password_input.login, password=user_password_input.password)
        if not user:
            raise Exception("Ошибка при регистрации пользователя.")
        return SignUp(user=UserObjectType(alias=user.meta_info.login))


class SignIn(graphene.Mutation):
    """Авторизация."""

    class Arguments:
        user_password_input = UserPasswordInput(required=True)

    token = graphene.String()

    async def mutate(self, info, user_password_input: UserPasswordInput):
        repository = UserRepository(info.context.get("client_motor"))
        user = await repository.check_user(login=user_password_input.login, password=user_password_input.password)
        if not user:
            raise Exception("Ошибка при авторизации пользователя.")
        token = Token(repository_user=repository, login=user.meta_info.login)
        return SignIn(token=token.encode())


class Refresh(graphene.Mutation):
    """Обновление токена."""
    token = graphene.String()

    @need_auth
    async def mutate(self, info):
        user: User = info.context.get("current_user")
        repository = UserRepository(info.context.get("client_motor"))
        token = Token(repository_user=repository, login=user.meta_info.login)
        return Refresh(token=token.encode())


class UserMutation(graphene.ObjectType):
    sign_up = SignUp.Field()
    sign_in = SignIn.Field()
    refresh = Refresh.Field()
