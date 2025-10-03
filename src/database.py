import sqlite3
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextvars import ContextVar

import aiosqlite

from src.config import settings

connection: ContextVar[aiosqlite.Connection] = ContextVar("connection")


async def connect() -> AsyncGenerator[aiosqlite.Connection]:
    """Primary function to init DB connection."""
    async with aiosqlite.connect(settings.sqlite_path, autocommit=sqlite3.LEGACY_TRANSACTION_CONTROL) as conn:
        connection.set(conn)
        yield conn


# To use in sync interface of app for init DB session.
db_connection_context_manager = asynccontextmanager(connect)


class BaseRepo:
    def __init__(self) -> None:
        self.conn: aiosqlite.Connection = connection.get()
