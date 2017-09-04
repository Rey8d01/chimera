"""Утилиты для работы с токенами."""

from jose import jwt

# todo вынести секрет
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_NAME_HEADER = "token"


def encode_token(claims: dict) -> str:
    """Общий механизм шифрования полезной информации в токен."""
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Общий механизм извлечения полезной информации из токена."""
    return jwt.decode(token=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
