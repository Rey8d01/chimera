from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.security import decode_token

from .repository import AuthUser
from .service import get_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> AuthUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = decode_token(token)
        user_id = int(data.get("sub", 0))
    except Exception:
        raise credentials_exception

    if not user_id:
        raise credentials_exception

    user = await get_by_id(user_id)
    if not user:
        raise credentials_exception
    return user
