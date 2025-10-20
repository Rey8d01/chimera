from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from src.config import settings
from src.logger import logger

from . import service
from .dependency import get_current_user
from .repository import AuthUser
from .schema import TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenOut:
    token = await service.login(form_data.username, SecretStr(form_data.password))
    return TokenOut(access_token=token)


@router.get("/me")
async def me(user: Annotated[AuthUser, Depends(get_current_user)]) -> UserOut:
    return UserOut(id=user["id"], email=user["email"], role=user["role"])


@router.get("/log-settings")
async def log_settings(_: Annotated[AuthUser, Depends(get_current_user)]) -> str:
    logger.debug(settings)
    return settings.model_dump_json()
