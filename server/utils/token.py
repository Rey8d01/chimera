"""Утилиты для работы с токенами."""

from jose import jwt

# todo вынести секрет
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_NAME_HEADER = "token"


def encode_token(claims):
    # claims = {"who": "user.meta_info.user"}
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    # token = self.request.headers.get(JWT_NAME_HEADER)
    # claims = None
    # if token:
    return jwt.decode(token=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
