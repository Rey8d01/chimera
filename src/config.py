from typing import ClassVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict()

    debug: bool = False
    demo_env: str = "From config.py"
    app_name: str = "chimera"
    app_description: str = "Python project example in docker"

    sqlite_path: str = "/app/db/data/app.sqlite"
    jwt_algo: str = "HS256"
    jwt_secret: SecretStr = SecretStr("change-me")
    password_pepper: SecretStr = SecretStr("change-me-too")


settings = Settings()
