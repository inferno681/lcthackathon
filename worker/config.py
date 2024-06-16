from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POOL_TIMEOUT: int
    POOL_SIZE: int
    GPU_HOST: str
    WHISPER_HOST: str
    REDIS_HOST: str
    REDIS_PORT: int
    SCREENSHOT_UPLOAD_LINK: str
    EMBEDDINGS_PORT: int
    OLLAMA_HOST: str
    OLLAMA_PORT: int
    OPENAI_PORT: int
    TEMP_PATH: str

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

    @property
    def OLLAMA_URL(self):
        return f"{self.OLLAMA_HOST}:{self.OLLAMA_PORT}"

    @property
    def OPENAI_URL(self):
        return f"{self.WHISPER_HOST}:{self.OPENAI_PORT}/v1/"

    @property
    def EMBEDDINGS_URL(self):
        return f"{self.GPU_HOST}:{self.EMBEDDINGS_PORT}"


config = Settings()
