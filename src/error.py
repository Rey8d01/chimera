# pyright: basic
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.auth.error import AuthError, UserAlreadyExistsError


def install_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistsError)
    def exists(_request: Request, _exc: UserAlreadyExistsError) -> JSONResponse:
        return JSONResponse({"detail": "Email already exists"}, status_code=409)

    @app.exception_handler(AuthError)
    def auth(_request: Request, _exc: AuthError) -> JSONResponse:
        return JSONResponse({"detail": "Invalid credentials"}, status_code=401)


class SecurityError(Exception):
    """Raised when a security issue occurs."""
