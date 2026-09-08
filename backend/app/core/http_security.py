"""
backend/app/core/http_security.py

Response security headers for the API.

Scope note: this is a JSON API consumed cross-origin by a Next.js SPA,
not an HTML app. That shapes every choice here — the headers that matter
are the ones limiting what a browser will do with an API *response* that
an attacker has coaxed it into rendering directly (a reflected error page,
a JSON body sniffed as HTML), plus transport security. The page-level CSP
that protects the actual UI has to be set by the frontend on its own
HTML responses; see frontend/next.config.js.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings

# `default-src 'none'` is the right policy for an API: no response from
# this service should ever legitimately load a script, style, image or
# frame. If a response somehow gets rendered as a document, nothing in it
# executes. frame-ancestors 'none' is the modern X-Frame-Options and
# blocks clickjacking of any HTML this service does return (the /docs
# page in non-production).
_API_CSP = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"

# FastAPI's Swagger/ReDoc pages pull their JS and CSS from jsdelivr, so
# the strict policy above would break them. They only exist outside
# production (see main.py), so this looser policy never ships.
_DOCS_CSP = (
    "default-src 'none'; "
    "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "img-src 'self' https://fastapi.tiangolo.com data:; "
    "font-src 'self' https://cdn.jsdelivr.net; "
    "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"
)

_DOCS_PATHS = ("/docs", "/redoc", "/openapi.json")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        headers = response.headers

        is_docs = request.url.path.startswith(_DOCS_PATHS)
        headers.setdefault("Content-Security-Policy", _DOCS_CSP if is_docs else _API_CSP)

        # Stops a browser from second-guessing our Content-Type and
        # treating a JSON body containing HTML as a document to render.
        headers.setdefault("X-Content-Type-Options", "nosniff")
        headers.setdefault("X-Frame-Options", "DENY")
        # Never leak a full API URL (which can carry ids) to a third party.
        headers.setdefault("Referrer-Policy", "no-referrer")
        # This API needs none of these; deny them rather than inherit
        # whatever the embedding context permits.
        headers.setdefault(
            "Permissions-Policy",
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()",
        )
        # Authenticated JSON must not sit in a shared cache.
        headers.setdefault("Cache-Control", "no-store")
        headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        headers.setdefault("Cross-Origin-Resource-Policy", "same-site")

        if settings.is_production:
            # Only meaningful over HTTPS, and actively harmful in local
            # dev (it would pin http://localhost to https for six months
            # in the developer's browser).
            headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains; preload",
            )

        # Server banner: version disclosure buys an attacker free recon.
        if "server" in headers:
            headers["server"] = "api"

        return response
