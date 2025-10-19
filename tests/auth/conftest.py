from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid1

import pytest_asyncio
from pydantic import SecretStr

from src.auth.repository import AuthUserRepo
from src.security import hash_password

if TYPE_CHECKING:
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
