"""Application settings."""

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    class Config:  # noqa: WPS431
        env_file = ".env"

    # base kwargs
    DEBUG: bool = False


settings = AppSettings()
