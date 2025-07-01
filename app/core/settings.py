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

<<<<<<< Updated upstream
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "moretti-customer", 
    POSTGRES_PASSWORD: str = "moretti"
    POSTGRES_DB: str = "product_db"
=======
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5434
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    CUSTOMER_API_KEY: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_DAYS: int
    CUSTOMER_API_KEY: str = ""
    CUSTOMER_API: str = ""
>>>>>>> Stashed changes

settings = Settings()  