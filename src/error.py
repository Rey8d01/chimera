# pyright: basic
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.auth.error import AuthFailed, UserAlreadyExists


def install_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExists)
    def exists(_request: Request, _exc: UserAlreadyExists) -> JSONResponse:
        return JSONResponse({"detail": "Email already exists"}, status_code=409)

    @app.exception_handler(AuthFailed)
    def auth(_request: Request, _exc: AuthFailed) -> JSONResponse:
        return JSONResponse({"detail": "Invalid credentials"}, status_code=401)


class SecurityError(Exception):
    """Raised when a security issue occurs."""
