from __future__ import annotations

import re
from typing import TYPE_CHECKING

from pydantic import SecretStr

from src import security
from src.auth.command import cli_app as auth_cli_app
from src.auth.repository import AuthUserRepo
from tests.utils import invoke_cli

if TYPE_CHECKING:
    from aiosqlite import Connection

    from src.auth.repository import AuthUser


async def test_create_user_cli_integration(test_database: Connection) -> None:  # pyright: ignore[reportUnusedParameter]
    email = "user@example.com"

    result = await invoke_cli(auth_cli_app, "create-user", email)

    assert result.exit_code == 0
    match = re.fullmatch(
        r"User created\. User ID: (\d+) Email: user@example\.com password: (.+)\n",
        result.stdout,
    )
    assert match is not None
    user_id = int(match.group(1))
    plain_password = match.group(2)

    auth_user_repo: AuthUserRepo = AuthUserRepo()
    auth_user = await auth_user_repo.get_by_id(user_id)
    assert auth_user is not None
    assert user_id == auth_user["id"]
    assert email == auth_user["email"]
    assert security.check_password(SecretStr(plain_password), auth_user["pwd"]) is True


async def test_flush_password_cli_integration(registered_user: AuthUser) -> None:
    flush_result = await invoke_cli(auth_cli_app, "flush-password", registered_user["email"])

    assert flush_result.exit_code == 0
    flush_match = re.fullmatch(
        rf"Password flushed\. Email: {re.escape(registered_user['email'])} password: (.+)\n",
        flush_result.stdout,
    )
    assert flush_match is not None
    new_password = flush_match.group(1)

    auth_user_repo: AuthUserRepo = AuthUserRepo()
    updated_user = await auth_user_repo.get_by_id(registered_user["id"])
    assert updated_user is not None

    assert updated_user["pwd"] != registered_user["pwd"]
    assert security.check_password(SecretStr(new_password), updated_user["pwd"]) is True
