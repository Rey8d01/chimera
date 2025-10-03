import typer

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
    print(f"User created. User ID: {user_id} Email: {register_user_in.email} password: {password.get_secret_value()}")


@cli_app.command()
@async_cli_runner
async def flush_password(email: str) -> None:
    password = generate_password()
    register_user_in = RegisterUserIn(email=email, password=password)
    await service.flush_password(email=register_user_in.email, new_password=register_user_in.password)
    print(f"Password flushed. Email: {register_user_in.email} password: {password.get_secret_value()}")
