import base64
import hashlib
import hmac
import os
import random
import secrets
import string
from datetime import UTC, datetime, timedelta
from typing import cast

import jwt
from pydantic import SecretStr

from src.config import settings
from src.error import SecurityError

PBKDF2_ITER = 310_000


def _pepper_password(p: SecretStr) -> bytes:
    """Return password bytes peppered with HMAC-SHA256."""
    key = settings.password_pepper.get_secret_value()
    return hmac.new(key.encode(), p.get_secret_value().encode(), hashlib.sha256).digest()


def hash_password(p: SecretStr) -> str:
    salt = os.urandom(16)
    pwd = _pepper_password(p)
    dk = hashlib.pbkdf2_hmac("sha256", pwd, salt, PBKDF2_ITER)
    return f"pbkdf2_sha256${PBKDF2_ITER}${base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"


def check_password(p: SecretStr, stored: str) -> bool:
    try:
        algo, iters, salt_b64, hash_b64 = stored.split("$", 3)
        if algo != "pbkdf2_sha256":
            return False
        pwd = _pepper_password(p)
        dk = hashlib.pbkdf2_hmac("sha256", pwd, base64.b64decode(salt_b64), int(iters))
        return hmac.compare_digest(dk, base64.b64decode(hash_b64))
    except Exception:
        return False


def create_access_token(sub: str, ttl: timedelta | None = None) -> str:
    if ttl is None:
        ttl = timedelta(minutes=15)
    now = datetime.now(tz=UTC)
    payload = {"sub": sub, "type": "access", "iat": now, "nbf": now, "exp": now + ttl}
    return jwt.encode(payload, settings.jwt_secret.get_secret_value(), algorithm=settings.jwt_algo)


def decode_token(token: str) -> dict[str, int | str]:
    return cast(
        "dict[str, int | str]",
        jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms=[settings.jwt_algo]),
    )


def generate_password(
    length: int = 20,
    *,
    min_upper: int = 1,
    min_lower: int = 1,
    min_digits: int = 1,
    min_symbols: int = 1,
) -> SecretStr:
    """Generate a strong random password using standard library helpers.

    Ensures minimum counts per class and shuffles via SystemRandom.
    """
    U, L, D, S = (
        string.ascii_uppercase,
        string.ascii_lowercase,
        string.digits,
        string.punctuation,
    )

    need = min_upper + min_lower + min_digits + min_symbols
    if length < need:
        raise SecurityError("length < sum of minimum requirements")

    parts = (
        [secrets.choice(U) for _ in range(min_upper)]
        + [secrets.choice(L) for _ in range(min_lower)]
        + [secrets.choice(D) for _ in range(min_digits)]
        + [secrets.choice(S) for _ in range(min_symbols)]
    )
    parts += [secrets.choice(U + L + D + S) for _ in range(length - need)]

    random.SystemRandom().shuffle(parts)
    return SecretStr("".join(parts))
