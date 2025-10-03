from typing import Protocol, TypedDict, cast

import aiosql
from aiosqlite import Connection

from src.database import BaseRepo


class AuthUser(TypedDict):
    id: int
    email: str
    pwd: str
    role: str
    created_at: str


class UserQueries(Protocol):
    async def create(self, conn: Connection, email: str, pwd: str, role: str) -> int: ...
    async def update_password(self, conn: Connection, auth_user_id: int, new_pwd: str) -> None: ...
    async def get_by_email(self, conn: Connection, email: str) -> tuple[int, str, str, str, str] | None: ...
    async def get_by_id(self, conn: Connection, auth_user_id: int) -> tuple[int, str, str, str, str] | None: ...


queries: UserQueries = cast("UserQueries", aiosql.from_path("src/auth/queries.sql", "aiosqlite"))


class AuthUserRepo(BaseRepo):
    async def create(self, email: str, pwd_hash: str, role: str = "user") -> int:
        user_id = await queries.create(self.conn, email=email, pwd=pwd_hash, role=role)
        await self.conn.commit()
        return user_id

    async def update_password(self, auth_user_id: int, new_pwd_hash: str) -> None:
        await queries.update_password(self.conn, auth_user_id=auth_user_id, new_pwd=new_pwd_hash)
        await self.conn.commit()

    async def get_by_email(self, email: str) -> AuthUser | None:
        row = await queries.get_by_email(self.conn, email=email)
        return (
            AuthUser(
                id=row[0],
                email=row[1],
                pwd=row[2],
                role=row[3],
                created_at=row[4],
            )
            if row
            else None
        )

    async def get_by_id(self, auth_user_id: int) -> AuthUser | None:
        row = await queries.get_by_id(self.conn, auth_user_id=auth_user_id)
        return (
            AuthUser(
                id=row[0],
                email=row[1],
                pwd=row[2],
                role=row[3],
                created_at=row[4],
            )
            if row
            else None
        )
