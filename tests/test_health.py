from http import HTTPStatus

from httpx import AsyncClient


async def test_health_returns_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "Ok"}
