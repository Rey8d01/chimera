from __future__ import annotations

from typing import TYPE_CHECKING

from src.security import check_password, create_access_token, hash_password

from .error import AuthFailed, UserAlreadyExists
from .repository import AuthUserRepo

if TYPE_CHECKING:
    from pydantic import SecretStr

    from .repository import AuthUser


async def register(email: str, password: SecretStr) -> int:
    auth_user_repo: AuthUserRepo = AuthUserRepo()

    if await auth_user_repo.get_by_email(email):
        raise UserAlreadyExists()

    return await auth_user_repo.create(email, hash_password(password))


async def flush_password(email: str, new_password: SecretStr) -> None:
    auth_user_repo: AuthUserRepo = AuthUserRepo()

    row = await auth_user_repo.get_by_email(email)
    if not row:
        raise AuthFailed()

    await auth_user_repo.update_password(row["id"], hash_password(new_password))


async def login(email: str, password: SecretStr) -> str:
    auth_user_repo = AuthUserRepo()

    row = await auth_user_repo.get_by_email(email)
    if not row or not check_password(password, row["pwd"]):
        raise AuthFailed()

    return create_access_token(sub=str(row["id"]))


async def get_by_id(auth_user_id: int) -> AuthUser | None:
    return await AuthUserRepo().get_by_id(auth_user_id)
