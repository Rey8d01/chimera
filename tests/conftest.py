from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from db.migrate_sqlite import migrate  # noqa: E402
from src.config import settings  # noqa: E402
from src.database import db_connection_context_manager  # noqa: E402
from src.main import web_app  # noqa: E402

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from aiosqlite import Connection


@pytest_asyncio.fixture
async def test_database(tmp_path: Path) -> AsyncIterator[Connection]:
    test_db_path = tmp_path / "test.sqlite"
    settings.sqlite_path = str(test_db_path)

    await migrate(db_path=test_db_path)

    async with db_connection_context_manager() as conn:
        yield conn


@pytest_asyncio.fixture
async def async_client(test_database: Connection) -> AsyncIterator[AsyncClient]:  # pyright: ignore[reportUnusedParameter]
    transport = ASGITransport(app=web_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
