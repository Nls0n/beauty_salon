from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str = Field(default="admin")
    password: str = Field(default="admin")
    name: str = Field(default="beauty_db")
    port: int = 5432
    host: str = Field(default="localhost")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


SETTINGS = Settings()

__all__ = ["SETTINGS"]
