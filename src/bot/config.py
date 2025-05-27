from pydantic import SecretStr
from pydantic_settings import BaseSettings

from bot.internal.helpers import assign_config_dict


class BotConfig(BaseSettings):
    ADMIN: int
    TOKEN: SecretStr
    CHANNEL_ID: int
    CHANNEL_LINK: str

    model_config = assign_config_dict(prefix="BOT_")


class DBConfig(BaseSettings):
    NAME: str
    echo: bool = False

    model_config = assign_config_dict(prefix="DB_")

    @property
    def aiosqlite_db_url(self) -> str:
        return f"sqlite+aiosqlite:///src/database/{self.NAME}.db"


class Settings(BaseSettings):
    bot: BotConfig = BotConfig()
    db: DBConfig = DBConfig()

    model_config = assign_config_dict()


settings = Settings()
