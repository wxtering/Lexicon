from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / "cfg.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class BotConfig(ConfigBase):
    bot_token: SecretStr


def get_bot_config() -> BotConfig:
    return BotConfig()


class DatabaseConfig(ConfigBase):
    db_url: str
    db_echo: bool = False


def get_database_config() -> DatabaseConfig:
    return DatabaseConfig()
