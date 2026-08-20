from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # ─── App ──────────────────────────────────────────────────────────────
    APP_NAME: str = "AI Career Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    # ─── Security ─────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # ─── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_career_platform"

    # ─── AI provider ──────────────────────────────────────────────────────
    GENERATION_BACKEND: str = "anthropic"
    GENERATION_MODEL_ID: str = "claude-sonnet-4-20250514"
    GENERATION_DEFAULT_MAX_TOKENS: int = 1000
    GENERATION_DEFAULT_TEMPERATURE: float = 0.7
    INPUT_DEFAULT_MAX_CHARACTERS: int = 10000

    # ─── API keys ─────────────────────────────────────────────────────────
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_URL: Optional[str] = None

    # ─── Embedding / Vector DB (future) ───────────────────────────────────
    EMBEDDING_BACKEND: Optional[str] = None
    EMBEDDING_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_SIZE: Optional[int] = None
    VECTOR_DB_BACKEND: Optional[str] = None
    VECTOR_DB_PATH: Optional[str] = None
    VECTOR_DB_DISTANCE_METHOD: Optional[str] = None

    # ─── Localisation ─────────────────────────────────────────────────────
    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"

    # ─── CORS ─────────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"
    # Comma-separated list of extra allowed origins for production
    # (staging domains, custom domains, etc.), e.g. "https://app.example.com,https://staging.example.com"
    EXTRA_CORS_ORIGINS: str = ""

    # ─── Email (Resend) ──────────────────────────────────────────────────────
    RESEND_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "AI Career Platform <noreply@example.com>"

    # ─── Payments (Paymob) ─────────────────────────────────────────────────
    PAYMOB_API_KEY: Optional[str] = None
    PAYMOB_INTEGRATION_ID_CARD: Optional[str] = None
    PAYMOB_INTEGRATION_ID_WALLET: Optional[str] = None
    PAYMOB_IFRAME_ID: Optional[str] = None
    PAYMOB_HMAC_SECRET: Optional[str] = None
    PAYMOB_BASE_URL: str = "https://accept.paymob.com/api"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        origins = {self.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"}
        origins.update(o.strip() for o in self.EXTRA_CORS_ORIGINS.split(",") if o.strip())
        return sorted(origins)


# No lru_cache — always reads fresh from .env
settings = Settings()

# ─── Fail fast on unsafe production config ─────────────────────────────────
if settings.APP_ENV == "production":
    _problems = []
    if settings.SECRET_KEY == "change-me-in-production" or len(settings.SECRET_KEY) < 32:
        _problems.append("SECRET_KEY must be set to a random value of at least 32 characters")
    if "localhost" in settings.DATABASE_URL or "password@" in settings.DATABASE_URL:
        _problems.append("DATABASE_URL still points at the local dev database/credentials")
    if _problems:
        raise RuntimeError(
            "Refusing to start with APP_ENV=production due to unsafe configuration:\n  - "
            + "\n  - ".join(_problems)
        )