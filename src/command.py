import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps

from .database import db_connection_context_manager


def async_cli_runner[**P, R](func: Callable[P, Awaitable[R]]) -> Callable[P, R]:
    """Decorator to run an async function in a CLI context with DB setup.

    Wraps an async callable `func` and returns a sync callable preserving the
    original signature. Internally, it establishes a DB connection context and
    executes the coroutine via ``asyncio.run``.

    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # In API this is used via Depends by FastAPI, here we do it explicitly.
            async with db_connection_context_manager():
                return await func(*args, **kwargs)

        return asyncio.run(async_wrapper(*args, **kwargs))

    return wrapper
