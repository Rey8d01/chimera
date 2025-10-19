from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid1

import pytest
import pytest_asyncio
from pydantic import SecretStr

from src.auth.dependency import get_current_user
from src.auth.repository import AuthUserRepo
from src.main import web_app
from src.security import hash_password

if TYPE_CHECKING:
    from collections.abc import Iterator

    from aiosqlite import Connection

    from src.auth.repository import AuthUser

TEST_PASSWORD = "Password123!"


@pytest_asyncio.fixture
async def registered_user(test_database: Connection) -> AuthUser:  # pyright: ignore[reportUnusedParameter]
    email = f"user-{uuid1().hex}@example.com"

    auth_user_repo: AuthUserRepo = AuthUserRepo()
    user_id = await auth_user_repo.create(email, hash_password(SecretStr(TEST_PASSWORD)))
    auth_user = await auth_user_repo.get_by_id(user_id)
    assert auth_user is not None
    return auth_user


@pytest.fixture
def authorized_user(registered_user: AuthUser) -> Iterator[AuthUser]:
    def override_current_user() -> AuthUser:
        return registered_user

    web_app.dependency_overrides[get_current_user] = override_current_user
    try:
        yield registered_user
    finally:
        web_app.dependency_overrides.pop(get_current_user, None)
