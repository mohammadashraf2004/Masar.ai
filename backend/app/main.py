from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.limiter import limiter
from app.controllers import auth_controller, tracks_controller, mentor_controller, exam_controller, community_controller, profile_controller
from app.controllers.wallet_controller import router as wallet_router
from app.controllers.challenge_controller import router as challenge_router
from app.controllers.exam_payment_controller import router as exam_payment_router
from app.controllers.payments_controller import router as payments_router
from app.controllers.tool_courses_controller import router as tool_courses_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered career acceleration platform for tech students in MENA",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.APP_ENV != "production" else None,
)

# ─── Rate limiting ──────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth_controller.router,        prefix=API_PREFIX)
app.include_router(tracks_controller.router,      prefix=API_PREFIX)
app.include_router(mentor_controller.router,      prefix=API_PREFIX)
app.include_router(community_controller.router,   prefix=API_PREFIX)
app.include_router(exam_controller.router,        prefix=API_PREFIX)
app.include_router(profile_controller.router,     prefix=f"{API_PREFIX}/profile",       tags=["Profile"])
app.include_router(wallet_router,                 prefix=f"{API_PREFIX}/wallet",        tags=["Wallet"])
app.include_router(challenge_router,              prefix=f"{API_PREFIX}/challenges",    tags=["Challenges"])
app.include_router(exam_payment_router,           prefix=f"{API_PREFIX}/exam-payments", tags=["Exam Payments"])
app.include_router(payments_router,               prefix=f"{API_PREFIX}/payments",      tags=["Payments"])
app.include_router(tool_courses_router,           prefix=API_PREFIX)


# ─── Health ───────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    from sqlalchemy import text
    from app.db.session import SessionLocal
    from app.services.llm import LLMEnum

    backend = settings.GENERATION_BACKEND
    key_present = False
    if backend == LLMEnum.ANTHROPIC.value:
        key_present = bool(settings.ANTHROPIC_API_KEY)
    elif backend == LLMEnum.OPENAI.value:
        key_present = bool(settings.OPENAI_API_KEY)

    db_ok = True
    db_error = None
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_ok = False
        db_error = str(e)
    finally:
        db.close()

    body = {
        "status": "ok" if db_ok else "degraded",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "database": "ok" if db_ok else "unreachable",
        "ai_provider": backend,
        "ai_model": settings.GENERATION_MODEL_ID,
        "ai_key_configured": key_present,
    }
    if db_error and settings.APP_ENV != "production":
        body["database_error"] = db_error
    return JSONResponse(content=body, status_code=200 if db_ok else 503)


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "docs": "/docs", "health": "/health"}
