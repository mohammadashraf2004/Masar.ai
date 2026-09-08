import logging
import secrets
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core import security_log
from app.core.config import settings
from app.core.http_security import SecurityHeadersMiddleware
from app.core.limiter import limiter, verify_storage_reachable
from app.core.metrics import (
    MetricsMiddleware,
    record_rate_limit_hit,
    render_metrics,
    route_template,
)
from app.controllers import auth_controller, tracks_controller, mentor_controller, exam_controller, community_controller, profile_controller
from app.controllers.wallet_controller import router as wallet_router
from app.controllers.challenge_controller import router as challenge_router
from app.controllers.exam_payment_controller import router as exam_payment_router
from app.controllers.payments_controller import router as payments_router
from app.controllers.tool_courses_controller import router as tool_courses_router
from app.controllers.answer_evaluation_controller import router as answer_evaluation_router
from app.controllers.terminology_controller import router as terminology_router
from app.controllers.search_controller import router as search_router
from app.controllers.admin_analytics_controller import router as admin_analytics_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered career acceleration platform for tech students in MENA",
    version=settings.APP_VERSION,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)

# ─── Rate limiting ──────────────────────────────────────────────────────────
# Probe the backend before serving. A rate limiter whose storage is
# unreachable is not a degraded rate limiter, it is no rate limiter at
# all, so this must stop the process rather than log a warning.
verify_storage_reachable()
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    security_log.rate_limit_hit(path=request.url.path, ip=request.client.host if request.client else None)
    # Same template resolution the middleware uses, so a rate-limited route
    # is labelled identically to the same route when it succeeds.
    record_rate_limit_hit(route_template(request))
    return _rate_limit_exceeded_handler(request, exc)


app.add_middleware(SlowAPIMiddleware)


# ─── Unhandled errors ───────────────────────────────────────────────────────
def _server_error_response(request: Request, exc: Exception) -> JSONResponse:
    """The opaque 500 every unhandled exception turns into.

    A bug's details (SQL text, table names, file paths, connection strings)
    are reconnaissance, so the client gets an id and nothing else; the id,
    the traceback and the route go to the server log so support can join
    the two.
    """
    error_id = uuid.uuid4().hex[:12]
    security_log.server_error(error_id=error_id, path=request.url.path, method=request.method)
    logging.getLogger("app.error").exception("error_id=%s unhandled error", error_id, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_id": error_id},
    )


class UnhandledErrorMiddleware(BaseHTTPMiddleware):
    """Turns an unhandled exception into a 500 *inside* the middleware stack.

    FastAPI installs a handler registered for bare `Exception` on Starlette's
    ServerErrorMiddleware, which is the outermost layer of the whole app —
    outside CORSMiddleware and SecurityHeadersMiddleware. A 500 produced
    there is therefore sent with no Access-Control-Allow-Origin and none of
    our security headers, so a browser refuses to let the SPA read it: the
    frontend never saw the `error_id` below and could only report "could not
    reach the server", which is a different (and wrong) diagnosis.

    Catching here instead means the 500 travels back out through the normal
    stack and picks up both. Placement is deliberate and load-bearing:

      CORS -> SecurityHeaders -> [this] -> Metrics -> SlowAPI -> routes

    Outside Metrics, so MetricsMiddleware still sees the exception and keeps
    incrementing http_exceptions_total rather than just recording a 500.
    Inside CORS and SecurityHeaders, so both post-process the response.
    HTTPException, RateLimitExceeded and the SQLAlchemy handlers are all
    dealt with deeper in the stack and never reach this.

    The `Exception` handler further down is kept as the last-resort net for
    anything raised by the middleware *outside* this one.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:  # noqa: BLE001 — that is the point
            return _server_error_response(request, exc)


# ─── Metrics ────────────────────────────────────────────────────────────────
# Added before the security-headers middleware so the timing it records is
# the full time this app spent on the request, including everything the
# other middleware does.
if settings.METRICS_ENABLED:
    app.add_middleware(MetricsMiddleware)

# Added after MetricsMiddleware and before SecurityHeadersMiddleware, which
# puts it between the two in the stack. See the class docstring — the order
# is what makes a 500 come back with CORS and security headers on it while
# leaving the exception metric intact.
app.add_middleware(UnhandledErrorMiddleware)

# ─── Security headers ───────────────────────────────────────────────────────
app.add_middleware(SecurityHeadersMiddleware)

# ─── CORS ─────────────────────────────────────────────────────────────────────
# allow_credentials is on because the browser-side client may send an
# Authorization header; combined with an explicit origin allowlist (never
# "*", which the spec forbids alongside credentials anyway). Methods and
# headers are enumerated rather than "*" so a future exotic method can't
# be preflighted through.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
    max_age=600,
)


# ─── Error handling ──────────────────────────────────────────────────────────
# Anything that isn't a deliberate HTTPException is a bug, and a bug's
# details (SQL text, table names, file paths, connection strings) are
# reconnaissance. The client gets an opaque id; the id, the traceback and
# the route go to the server log so support can join the two.

@app.exception_handler(IntegrityError)
async def _integrity_error_handler(request: Request, exc: IntegrityError):
    error_id = uuid.uuid4().hex[:12]
    logging.getLogger("app.error").warning(
        "error_id=%s integrity error on %s %s", error_id, request.method, request.url.path,
        exc_info=exc,
    )
    # A unique/FK violation reaching this handler is virtually always a
    # duplicate or a stale reference the caller can fix themselves.
    return JSONResponse(
        status_code=409,
        content={"detail": "That change conflicts with existing data.", "error_id": error_id},
    )


@app.exception_handler(SQLAlchemyError)
async def _db_error_handler(request: Request, exc: SQLAlchemyError):
    error_id = uuid.uuid4().hex[:12]
    security_log.server_error(error_id=error_id, path=request.url.path, method=request.method)
    logging.getLogger("app.error").exception("error_id=%s database error", error_id)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_id": error_id},
    )


@app.exception_handler(Exception)
async def _unhandled_error_handler(request: Request, exc: Exception):
    # Last resort only. UnhandledErrorMiddleware catches everything raised
    # at or below the router, so what reaches here was raised by one of the
    # middleware outside it (CORS, security headers). Such a response cannot
    # get CORS headers — there is nothing left to add them — but it is far
    # better than a bare connection drop.
    return _server_error_response(request, exc)


@app.exception_handler(HTTPException)
async def _http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code in (401, 403):
        security_log.authz_denied(
            user_id=None,
            path=request.url.path,
            reason=f"http_{exc.status_code}",
        )
    return await http_exception_handler(request, exc)


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
app.include_router(answer_evaluation_router,      prefix=API_PREFIX)
app.include_router(terminology_router,            prefix=API_PREFIX)
app.include_router(search_router,                 prefix=API_PREFIX)
# Read-only admin analytics. Nothing else in the app imports it, so the
# rest of the API is unaffected if these queries ever misbehave.
app.include_router(admin_analytics_router,        prefix=API_PREFIX)


# ─── Metrics ──────────────────────────────────────────────────────────────────
if settings.METRICS_ENABLED:

    @app.get("/metrics", include_in_schema=False)
    def metrics(request: Request):
        """Prometheus exposition, aggregated across all gunicorn workers.

        Guarded by a bearer token because this port is published to the
        host: the payload maps every route, its latency and its error rate,
        plus credit burn and auth-failure counts. A wrong or missing token
        gets a 404 rather than a 401 — an unauthenticated caller should not
        even learn the endpoint exists.
        """
        expected = settings.METRICS_TOKEN
        if expected:
            header = request.headers.get("authorization", "")
            supplied = (
                header[7:] if header[:7].lower() == "bearer " else request.query_params.get("token", "")
            )
            if not secrets.compare_digest(supplied, expected):
                raise HTTPException(status_code=404, detail="Not Found")
        return render_metrics()


# ─── Health ───────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Deliberately minimal in production. A health endpoint is reachable
    by anyone who can reach the service at all, so it should confirm
    liveness without also publishing which AI vendor is in use, which
    model, whether a key is configured, or the database error text — all
    of which are free reconnaissance."""
    from sqlalchemy import text
    from app.db.session import SessionLocal

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
        "database": "ok" if db_ok else "unreachable",
    }

    if not settings.is_production:
        from app.services.llm import LLMEnum

        backend = settings.GENERATION_BACKEND
        key_present = False
        if backend == LLMEnum.ANTHROPIC.value:
            key_present = bool(settings.ANTHROPIC_API_KEY)
        elif backend == LLMEnum.OPENAI.value:
            key_present = bool(settings.OPENAI_API_KEY)
        body.update({
            "env": settings.APP_ENV,
            "ai_provider": backend,
            "ai_model": settings.GENERATION_MODEL_ID,
            "ai_key_configured": key_present,
        })
        if db_error:
            body["database_error"] = db_error

    return JSONResponse(content=body, status_code=200 if db_ok else 503)


@app.get("/", tags=["Root"])
def root():
    body = {"message": f"Welcome to {settings.APP_NAME} API", "health": "/health"}
    if not settings.is_production:
        body["docs"] = "/docs"
    return body
