import typer

from src.auth.command import cli_app as auth_cli_app

cli_app = typer.Typer()
cli_app.add_typer(auth_cli_app, name="auth")

if __name__ == "__main__":
    cli_app()
