import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    HOST: str
    PORT: int

    KAFKA_HOST: str
    KAFKA_PORT: str

    DEBUG: bool = Field(default=False)

    class Config:
        env_file = ".env"


class SettingsProd(Settings):
    class Config:
        env_file = "prod.env"


class SettingsDev(Settings):
    class Config:
        env_file = "dev.env"


config = dict(prod=SettingsProd, dev=SettingsDev)
settings: Settings = config[os.environ.get("APP_ENV", "dev").lower()]()  # type: ignore
