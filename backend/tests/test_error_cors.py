"""
Cross-origin behaviour of unhandled server errors.

The generic `Exception` handler FastAPI registers lives on Starlette's
ServerErrorMiddleware, which sits *outside* CORSMiddleware and
SecurityHeadersMiddleware. A 500 produced there went back without
Access-Control-Allow-Origin, so the browser refused to let the SPA read
it: the frontend never saw the `error_id` and reported "could not reach
the server" instead of a server fault it could quote to support.

app/main.py now catches unhandled exceptions in UnhandledErrorMiddleware,
placed inside CORS and the security headers but outside MetricsMiddleware.
These tests pin all three properties: the response is still opaque, it now
carries the CORS and security headers, and the exception metric still fires.
"""
import re

import pytest

from app.core.config import settings

ALLOWED_ORIGIN = "http://localhost:3000"
FOREIGN_ORIGIN = "https://evil.example.com"
BOOM_PATH = "/api/v1/__boom_for_tests__"
SECRET = "connection to users_private failed at 10.0.0.7"


@pytest.fixture()
def boom_route():
    """A route that raises, registered only for the test that asks for it.

    Deliberately a real route rather than a monkeypatched handler, so the
    exception travels the whole middleware stack exactly as a production
    bug would.
    """
    from app.main import app

    def _boom():
        raise RuntimeError(SECRET)

    app.add_api_route(BOOM_PATH, _boom, methods=["GET"], include_in_schema=False)
    try:
        yield BOOM_PATH
    finally:
        app.routes[:] = [r for r in app.routes if getattr(r, "path", None) != BOOM_PATH]


def test_the_allowed_origin_is_a_precondition():
    """If this ever stops holding, the assertions below prove nothing."""
    assert ALLOWED_ORIGIN in settings.cors_origins
    assert FOREIGN_ORIGIN not in settings.cors_origins


# ─────────────────────────────────────────────────────────────────────────
# 1. A 500 reaches the SPA — headers and error_id
# ─────────────────────────────────────────────────────────────────────────

def test_500_to_a_frontend_origin_carries_cors_headers(client, boom_route):
    """The regression. Without the CORS header the browser discards the
    response and the SPA cannot read the body at all."""
    resp = client.get(boom_route, headers={"Origin": ALLOWED_ORIGIN})

    assert resp.status_code == 500
    assert resp.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert resp.headers["access-control-allow-credentials"] == "true"


def test_500_body_carries_a_usable_error_id(client, boom_route):
    resp = client.get(boom_route, headers={"Origin": ALLOWED_ORIGIN})
    body = resp.json()

    assert body["detail"] == "Internal server error"
    assert re.fullmatch(r"[0-9a-f]{12}", body["error_id"]), body


def test_error_ids_are_unique_per_request(client, boom_route):
    """Support joins a user's report to one log line, so two failures must
    not share an id."""
    ids = {
        client.get(boom_route, headers={"Origin": ALLOWED_ORIGIN}).json()["error_id"]
        for _ in range(3)
    }
    assert len(ids) == 3


def test_500_stays_opaque(client, boom_route):
    """The whole point of the handler: the client learns nothing about the
    fault beyond an id."""
    resp = client.get(boom_route, headers={"Origin": ALLOWED_ORIGIN})

    assert set(resp.json()) == {"detail", "error_id"}
    assert SECRET not in resp.text
    assert "RuntimeError" not in resp.text
    assert "Traceback" not in resp.text


def test_500_still_carries_the_security_headers(client, boom_route):
    """SecurityHeadersMiddleware sits outside the new one, so an error
    response must be hardened like every other response."""
    resp = client.get(boom_route, headers={"Origin": ALLOWED_ORIGIN})

    assert resp.headers["x-content-type-options"] == "nosniff"
    assert resp.headers["x-frame-options"] == "DENY"
    assert resp.headers["referrer-policy"] == "no-referrer"
    assert "default-src 'none'" in resp.headers["content-security-policy"]


# ─────────────────────────────────────────────────────────────────────────
# 2. CORS is still a restriction, not a rubber stamp
# ─────────────────────────────────────────────────────────────────────────

def test_a_foreign_origin_is_still_refused_the_cors_header(client, boom_route):
    """Fixing the 500 path must not turn the allowlist into allow-all — an
    unlisted origin still gets no Access-Control-Allow-Origin, so the
    browser still refuses to hand it the body."""
    resp = client.get(boom_route, headers={"Origin": FOREIGN_ORIGIN})

    assert resp.status_code == 500
    assert "access-control-allow-origin" not in resp.headers


def test_a_foreign_origin_is_still_refused_on_a_normal_response(client):
    resp = client.get("/health", headers={"Origin": FOREIGN_ORIGIN})
    assert resp.status_code == 200
    assert "access-control-allow-origin" not in resp.headers


def test_preflight_from_the_frontend_still_works(client):
    resp = client.options(
        "/api/v1/wallet/costs",
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization",
        },
    )
    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


# ─────────────────────────────────────────────────────────────────────────
# 3. Nothing else about error handling moved
# ─────────────────────────────────────────────────────────────────────────

def test_deliberate_http_errors_are_unchanged(client):
    """HTTPException is handled deeper in the stack and must not be
    swallowed into an opaque 500 by the new middleware."""
    resp = client.get("/api/v1/no-such-endpoint", headers={"Origin": ALLOWED_ORIGIN})
    assert resp.status_code == 404
    assert "error_id" not in resp.json()
    assert resp.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_401_is_unchanged(client):
    resp = client.get("/api/v1/wallet/", headers={"Origin": ALLOWED_ORIGIN})
    assert resp.status_code == 401
    assert resp.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_health_is_unaffected(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert resp.json()["database"] == "ok"


def test_the_exception_metric_still_fires(client, boom_route):
    """UnhandledErrorMiddleware is placed OUTSIDE MetricsMiddleware
    precisely so the exception still propagates through it. If the two are
    ever reordered, http_exceptions_total silently stops counting and only
    this test says so."""
    if not settings.METRICS_ENABLED:
        pytest.skip("metrics disabled in this configuration")

    from app.core.metrics import http_exceptions_total

    def _raw_count():
        total = 0.0
        for metric in http_exceptions_total.collect():
            for sample in metric.samples:
                if sample.labels.get("exception") == "RuntimeError":
                    total += sample.value
        return total

    before = _raw_count()
    client.get(boom_route, headers={"Origin": ALLOWED_ORIGIN})
    assert _raw_count() == before + 1
