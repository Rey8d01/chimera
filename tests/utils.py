from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from typer.testing import CliRunner

if TYPE_CHECKING:
    from click.testing import Result
    from typer import Typer

runner = CliRunner()


async def invoke_cli(cli_app: Typer, *args: str) -> Result:
    """Run Typer CLI in a thread so asyncio.run can safely execute."""
    return await asyncio.to_thread(runner.invoke, cli_app, list(args))
