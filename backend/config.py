from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(dotenv_path=".env", override=True)


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASS: str
    REDIS_DB_CELERY_BROKER: int
    REDIS_DB_CELERY_RESULT: int
    REDIS_DB_CELERY_REDBEAT: int

    TELEGRAM_TOKEN: str

    @property
    def REDIS_URL_CELERY_REDBEAT(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY_REDBEAT}"

    @property
    def REDIS_URL_CELERY_BROKER(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY_BROKER}"

    @property
    def REDIS_URL_CELERY_RESULT(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY_RESULT}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings: Settings = Settings()
