from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # ─── App ──────────────────────────────────────────────────────────
    APP_NAME: str = "AI Career Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    # ─── Security ─────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # ─── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_career_platform"

    # ─── LLM Generation backend ───────────────────────────────────────
    GENERATION_BACKEND: str = "anthropic"           # "anthropic" | "openai"
    GENERATION_MODEL_ID: str = "claude-sonnet-4-20250514"
    GENERATION_DEFAULT_MAX_TOKENS: int = 1000
    GENERATION_DEFAULT_TEMPERATURE: float = 0.7
    INPUT_DEFAULT_MAX_CHARACTERS: int = 10000

    # ─── Provider API keys ────────────────────────────────────────────
    ANTHROPIC_API_KEY: str = None
    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None          # optional custom base URL

    # ─── Embedding backend (future use) ───────────────────────────────
    EMBEDDING_BACKEND: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    # ─── Vector DB (future use) ───────────────────────────────────────
    VECTOR_DB_BACKEND: str = None
    VECTOR_DB_PATH: str = None
    VECTOR_DB_DISTANCE_METHOD: str = None

    # ─── Localisation ─────────────────────────────────────────────────
    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"

    # ─── CORS ─────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
