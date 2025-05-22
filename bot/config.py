from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(dotenv_path=".env", override=True)


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings: Settings = Settings()
