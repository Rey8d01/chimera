from __future__ import annotations

from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING

import jwt
import pytest

from src.config import settings
from tests.auth.conftest import TEST_PASSWORD

if TYPE_CHECKING:
    from httpx import AsyncClient

    from src.auth.repository import AuthUser


LOGIN_URL = "/auth/login"
ME_URL = "/auth/me"
LOG_SETTINGS_URL = "/auth/log-settings"


async def test_login_success_returns_token(async_client: AsyncClient, registered_user: AuthUser) -> None:
    response = await async_client.post(
        LOGIN_URL, data={"username": registered_user["email"], "password": TEST_PASSWORD}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["token_type"] == "bearer"
    assert isinstance(response.json()["access_token"], str)


async def test_login_rejects_invalid_credentials(async_client: AsyncClient, registered_user: AuthUser) -> None:
    response = await async_client.post(LOGIN_URL, data={"username": registered_user["email"], "password": "wrong"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}


async def test_me_returns_current_user(async_client: AsyncClient, authorized_user: AuthUser) -> None:
    response = await async_client.get(ME_URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": authorized_user["id"], "email": authorized_user["email"], "role": "user"}


@pytest.mark.usefixtures("registered_user")
async def test_me_rejects_broken_token(async_client: AsyncClient) -> None:
    response = await async_client.get(ME_URL, headers={"Authorization": "Bearer broken token"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_me_rejects_token_without_sub(async_client: AsyncClient) -> None:
    now = datetime.now(tz=UTC)
    token = jwt.encode(
        {
            "type": "access",
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=5),
        },
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algo,
    )

    response = await async_client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_me_rejects_when_user_missing(async_client: AsyncClient) -> None:
    now = datetime.now(tz=UTC)
    token = jwt.encode(
        {
            "type": "access",
            "sub": "424242",
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=5),
        },
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algo,
    )

    response = await async_client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
