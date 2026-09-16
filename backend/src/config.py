from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embedding_provider: str = "sentence_transformers"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    mistral_api_key: str | None = None

    llm_provider: str = "gemini"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.1-flash-lite"
    
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()