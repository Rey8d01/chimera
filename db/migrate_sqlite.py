from __future__ import annotations

import asyncio
import pathlib
import sys
from typing import TYPE_CHECKING, Literal

import aiosqlite
from dotenv import load_dotenv

if TYPE_CHECKING:
    UP_DOWN = Literal["up", "down"]

load_dotenv()

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB_PATH = pathlib.Path(ROOT / "db" / "data" / "app.sqlite")
MIGR_DIR = ROOT / "db" / "migrations"

UP_MARK = "-- +migrate Up"
DOWN_MARK = "-- +migrate Down"


def ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


async def ensure_meta(conn: aiosqlite.Connection) -> None:
    await conn.execute("PRAGMA foreign_keys = ON;")
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
      id TEXT PRIMARY KEY,
      applied_at TEXT NOT NULL DEFAULT (datetime('now'))
    )
    """)
    await conn.commit()


async def get_applied(conn: aiosqlite.Connection) -> set[str]:
    rows = await conn.execute_fetchall("SELECT id FROM schema_migrations")
    return {r[0] for r in rows}


def parse_section(text: str, direction: UP_DOWN) -> str:
    """Cut out the block between the markers.

    For Up: content after -- +migrate Up up to -- +migrate Down (or end of file).
    For Down: content after -- +migrate Down up to the next Up (usually there isn't one).

    """
    if direction == "up":
        if UP_MARK not in text:
            raise RuntimeError("Migration missing Up section")
        body = text.split(UP_MARK, 1)[1]
        if DOWN_MARK in body:
            body = body.split(DOWN_MARK, 1)[0]
        return body.strip()

    if DOWN_MARK not in text:
        raise RuntimeError("Migration missing Down section")
    body = text.split(DOWN_MARK, 1)[1]
    if UP_MARK in body:
        body = body.split(UP_MARK, 1)[0]
    return body.strip()


async def apply_one(conn: aiosqlite.Connection, fname: str, sql_body: str, direction: UP_DOWN) -> None:
    # executescript выполняет несколько стейтментов разом; оборачиваем в явную транзакцию
    await conn.execute("BEGIN;")
    try:
        await conn.executescript("PRAGMA foreign_keys = ON;")
        if sql_body:
            await conn.executescript(sql_body)
        if direction == "up":
            await conn.execute("INSERT INTO schema_migrations(id) VALUES (?)", (fname,))
        else:
            await conn.execute("DELETE FROM schema_migrations WHERE id = ?", (fname,))
        await conn.execute("COMMIT;")
        print(f"{direction.upper()}: {fname}")
    except Exception as e:
        await conn.execute("ROLLBACK;")
        raise RuntimeError(f"Failed to apply {direction} {fname}: {e}") from e


async def migrate(direction: UP_DOWN = "up", steps: int | None = None) -> None:
    ensure_db_dir()

    async with aiosqlite.connect(DB_PATH) as conn:
        await ensure_meta(conn)
        applied = await get_applied(conn)

        files: list[str] = sorted(p.name for p in MIGR_DIR.glob("*.sql"))
        if direction == "down":
            files.reverse()

        left = steps if steps is not None else float("inf")
        for fname in files:
            want = (direction == "up" and fname not in applied) or (direction == "down" and fname in applied)
            if not want:
                continue
            text = (MIGR_DIR / fname).read_text(encoding="utf-8")
            body = parse_section(text, direction)
            await apply_one(conn, fname, body, direction)
            left -= 1
            if left == 0:
                break


if __name__ == "__main__":
    # Examples:
    #   python db/migrate_sqlite.py up
    #   python db/migrate_sqlite.py down 1
    direction: UP_DOWN = "up"
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        match arg:
            case "up" | "down":
                direction = arg
            case _:
                raise SystemExit("Usage: migrate_sqlite.py [up|down] [steps]")
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else None  # noqa: PLR2004
    asyncio.run(migrate(direction, steps))
