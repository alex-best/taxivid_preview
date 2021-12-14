from pathlib import Path
from typing import Any, Dict

import toml
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pydantic import BaseSettings
import aiohttp


def toml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    return toml.loads(Path('config.toml').read_text())


class Settings(BaseSettings):
    api_key: str
    admin: int
    yandex_api_key: str
    static_map_url: str
    geocode_url: str
    amplitude_url: str
    amplitude_key: str
    redirect_url: str
    uber_redirect_url: str
    api_url: str

    class Config:
        env_file_encoding = 'utf-8'

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                toml_config_settings_source,
                env_settings,
                file_secret_settings,
            )


settings = Settings()
messages = toml.loads(Path('messages.toml').read_text())
bot = Bot(settings.api_key, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
amplitude_session = aiohttp.ClientSession()
