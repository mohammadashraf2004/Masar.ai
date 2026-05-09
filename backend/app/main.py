from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.controllers import auth_controller, tracks_controller, mentor_controller

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered career acceleration platform for tech students in MENA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth_controller.router, prefix=API_PREFIX)
app.include_router(tracks_controller.router, prefix=API_PREFIX)
app.include_router(mentor_controller.router, prefix=API_PREFIX)


# ─── Health Check ────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "health": "/health",
    }
