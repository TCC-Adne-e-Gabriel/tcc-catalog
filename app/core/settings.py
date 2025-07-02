from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../env",        
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int
    POSTGRES_USER: str = "", 
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

settings = Settings()  