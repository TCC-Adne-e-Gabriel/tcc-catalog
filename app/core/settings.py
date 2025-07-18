from typing import Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../env",        
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5434
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    CUSTOMER_API_KEY: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_DAYS: int = 0
    CUSTOMER_API_KEY: str = ""
    CUSTOMER_API: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  