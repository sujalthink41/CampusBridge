from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from ...data.enums.config import Environments, LogLevel

env_file = Path(__file__).parent.parent.parent.parent.parent / ".env"

class AppSettings(BaseSettings):

    APP_NAME: str = Field(...)
    APP_URL: str = Field(...)

    DATABASE_URL: str = Field(...)
    ALLOW_ORIGINS: str = Field(...)

    ENVIRONMENT: Environments = Environments.development
    LOG_LEVEL: LogLevel = LogLevel.INFO

    ALGORITHM:str = Field(...)

    @property
    def allowed_origins(self):
        return [x.strip() for x in self.ALLOW_ORIGINS.split(",") if x.strip()]

    @property
    def is_production(self):
        return self.ENVIRONMENT == Environments.production

    model_config = {"env_file": env_file, "extra": "ignore"}


@lru_cache
def _get_app_settings():
    return AppSettings()

app_settings = _get_app_settings()