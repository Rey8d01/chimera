from __future__ import annotations

import json
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from src.config import settings

if TYPE_CHECKING:
    from httpx import AsyncClient

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
ME_URL = "/auth/me"
LOG_SETTINGS_URL = "/auth/log-settings"


async def register_user(async_client: AsyncClient, email: str, password: str) -> int:
    response = await async_client.post(REGISTER_URL, json={"email": email, "password": password})
    response.raise_for_status()
    data = response.json()
    assert "id" in data
    return int(data["id"])


async def login_user(async_client: AsyncClient, email: str, password: str) -> str:
    response = await async_client.post(
        LOGIN_URL,
        data={"username": email, "password": password},
    )
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    return str(payload["access_token"])


async def test_register_creates_user(async_client: AsyncClient) -> None:
    response = await async_client.post(REGISTER_URL, json={"email": "user@example.com", "password": "Secret123!"})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] > 0


async def test_register_duplicate_email_returns_conflict(async_client: AsyncClient) -> None:
    payload = {"email": "dup@example.com", "password": "Secret123!"}
    first = await async_client.post(REGISTER_URL, json=payload)
    assert first.status_code == HTTPStatus.OK

    duplicate = await async_client.post(REGISTER_URL, json=payload)

    assert duplicate.status_code == HTTPStatus.CONFLICT
    assert duplicate.json() == {"detail": "Email already exists"}


async def test_login_returns_token_for_valid_credentials(async_client: AsyncClient) -> None:
    email = "auth@example.com"
    password = "Password123!"
    await register_user(async_client, email, password)

    response = await async_client.post(LOGIN_URL, data={"username": email, "password": password})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["token_type"] == "bearer"
    assert isinstance(response.json()["access_token"], str)


async def test_login_with_invalid_credentials_returns_unauthorized(async_client: AsyncClient) -> None:
    email = "invalid@example.com"
    password = "Password123!"
    await register_user(async_client, email, password)

    response = await async_client.post(LOGIN_URL, data={"username": email, "password": "wrong"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}


async def test_me_returns_authenticated_user(async_client: AsyncClient) -> None:
    email = "me@example.com"
    password = "Password123!"
    user_id = await register_user(async_client, email, password)
    token = await login_user(async_client, email, password)

    response = await async_client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": user_id, "email": email, "role": "user"}


async def test_log_settings_requires_authentication(async_client: AsyncClient) -> None:
    response = await async_client.get(LOG_SETTINGS_URL)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


async def test_log_settings_returns_serialized_settings(async_client: AsyncClient) -> None:
    email = "settings@example.com"
    password = "Password123!"
    await register_user(async_client, email, password)
    token = await login_user(async_client, email, password)

    response = await async_client.get(LOG_SETTINGS_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK
    encoded_settings = response.json()
    assert isinstance(encoded_settings, str)
    decoded = json.loads(encoded_settings)
    assert decoded["app_name"] == settings.app_name
