"""Утилиты для работы с токенами."""

from datetime import datetime, timedelta
from typing import Union
from jose import jwt
from jose.exceptions import JWTError
from modules.user.repositories import UserRepository
from modules.user.domains import User

# todo вынести секрет
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_NAME_HEADER = "token"
JWT_EXP_TIMEDELTA = timedelta(days=1)


class Token:
    """Класс токена для авторизации клиента."""

    __slots__ = ("repository", "login", "exp")

    def __init__(self, repository_user: UserRepository, login: str, exp: float = None):
        self.repository = repository_user
        self.login = login
        self.exp = (datetime.now() + JWT_EXP_TIMEDELTA).timestamp() if exp is None else float(exp)

    def __str__(self):
        return jwt.encode(claims=self.as_claims(), key=JWT_SECRET, algorithm=JWT_ALGORITHM)

    def as_claims(self) -> dict:
        """Данные токена в виде словаря."""
        return {
            "login": self.login,
            "exp": self.exp
        }

    async def is_valid(self) -> bool:
        """Проверки корректности токена"""
        user = await self.get_user()
        if user is None:
            return False
        if not user.meta_info.is_active:
            return False
        if self.exp < datetime.now().timestamp():
            return False
        return True

    async def get_user(self) -> User:
        """Вернет модель пользователя закрепленного за токеном."""
        user = await self.repository.get_user(filters={"metaInfo.login": self.login})
        return user

    def encode(self) -> str:
        """Общий механизм шифрования полезной информации в токен."""
        return str(self)

    @classmethod
    def decode_from_str(cls, repository_user: UserRepository, token: str) -> 'Token':
        """Общий механизм извлечения полезной информации из токена.

        В случае проблем с декодированием выбрасывает исключение **JWTError**.

        """
        token_data = jwt.decode(token=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return cls(repository_user=repository_user, **token_data)
