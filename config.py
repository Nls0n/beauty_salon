from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    name: str = Field(default="beauty_db")
    port: int = 5432
    host: str = Field(default="localhost")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


SETTINGS = Settings()

__all__ = ["SETTINGS"]
