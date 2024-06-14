from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str
    APP_DESCRIPTION: str
    SECRET: SecretStr
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POOL_TIMEOUT: int
    POOL_SIZE: int
    EMBEDDINGS_SERVER: str
    REDIS_HOST: str
    REDIS_PORT: int
    MEDIA_FOLDER: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    @property
    def DATABASE_URL(self):
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


config = Settings()
