from fastapi import Depends, FastAPI

from src import database, error
from src.auth.router import router as auth_router
from src.config import settings

web_app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version="1",
    dependencies=[Depends(database.connect)],
)
error.install_handlers(web_app)
web_app.include_router(auth_router)


@web_app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "Ok"}


@web_app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@web_app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None) -> dict[str, str | int | None]:
    return {"item_id": item_id, "q": q}
