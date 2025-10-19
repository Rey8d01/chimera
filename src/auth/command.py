import rich
import typer
from rich.markup import escape

from src.command import async_cli_runner
from src.security import generate_password

from . import service
from .schema import RegisterUserIn

cli_app = typer.Typer()


@cli_app.command()
@async_cli_runner
async def create_user(email: str) -> None:
    password = generate_password()
    register_user_in = RegisterUserIn(email=email, password=password)
    user_id = await service.register(email=register_user_in.email, password=register_user_in.password)
    rich.print(
        f"User created. User ID: [bold]{user_id}[/bold] Email: [bold]{register_user_in.email}[/bold] password: [bold]{escape(password.get_secret_value())}[/bold]"
    )


@cli_app.command()
@async_cli_runner
async def flush_password(email: str) -> None:
    password = generate_password()
    register_user_in = RegisterUserIn(email=email, password=password)
    await service.flush_password(email=register_user_in.email, new_password=register_user_in.password)
    rich.print(
        f"Password flushed. Email: [bold]{register_user_in.email}[/bold] password: [bold]{escape(password.get_secret_value())}[/bold]"
    )
