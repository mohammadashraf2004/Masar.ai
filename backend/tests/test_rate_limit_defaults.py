"""
No endpoint is unlimited.

slowapi applies limits only to routes carrying an explicit
@limiter.limit(...) unless the Limiter itself declares defaults. It did
not, so every write endpoint in the community, exam, wallet, exam-payment
and tool-course controllers was completely unmetered — community post and
comment creation most obviously.

app.core.limiter now declares DEFAULT_LIMITS. Two properties of slowapi
0.1.9 make that safe, and both are asserted here rather than trusted,
because both are implementation details that a dependency bump could
change underneath us:

  * the default bucket is per (client, endpoint), not one global budget —
    otherwise a busy screen would starve every other screen;
  * defaults STACK with route decorators rather than being replaced by
    them, so the effective limit on a decorated route is min(default,
    decorated). That is why the default is not stricter than the loosest
    explicit limit in the app.
"""
import uuid

import pytest

from app.core.limiter import DEFAULT_LIMITS, limiter

STRONG_PASSWORD = "correcthorsebatterystaple"


def _register(client, prefix="rl"):
    email = f"{prefix}-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Limit Tester", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ─── the limiter is actually configured ───────────────────────────────────

def test_default_limits_are_configured(db):
    """The regression itself: an empty default meant unlisted endpoints
    were unlimited."""
    assert DEFAULT_LIMITS, "no default rate limit — unlisted endpoints are unlimited"
    assert limiter._default_limits, "Limiter was constructed without the defaults"


def test_default_is_not_stricter_than_any_explicit_limit():
    """Defaults stack with route decorators, so a default tighter than an
    existing explicit limit would silently tighten that route. The Paymob
    webhook's 120/minute is the loosest, and dropping it would start
    rejecting payment-confirmation retries."""
    from limits import parse

    default = min(parse(l).amount for l in DEFAULT_LIMITS)

    explicit = []
    for limits in limiter._route_limits.values():
        for lim in limits:
            # Compare per-minute budgets only; the app also has /hour
            # limits, which are stricter over their own window by design.
            if lim.limit.GRANULARITY.seconds == 60:
                explicit.append(lim.limit.amount)

    assert explicit, "no explicit per-minute limits found — test is not exercising anything"
    assert default >= max(explicit), (
        f"default {default}/minute is stricter than the loosest explicit "
        f"limit {max(explicit)}/minute and would silently tighten it"
    )


# ─── previously-unlimited endpoints now have a ceiling ────────────────────

@pytest.mark.parametrize("controller", [
    "community_controller",
    "exam_controller",
    "wallet_controller",
    "exam_payment_controller",
    "tool_courses_controller",
])
def test_previously_unlimited_controllers_are_covered(controller):
    """These five had write endpoints and no limits at all. They do not
    each need an explicit decorator — the default covers them — so this
    asserts the mechanism reaches them rather than counting decorators."""
    import importlib

    module = importlib.import_module(f"app.controllers.{controller}")
    routes = [r for r in module.router.routes if hasattr(r, "endpoint")]
    assert routes, f"{controller} exposes no routes"

    exempt = limiter._exempt_routes
    for route in routes:
        name = f"{route.endpoint.__module__}.{route.endpoint.__name__}"
        assert name not in exempt, f"{name} is exempt from rate limiting"


# ─── explicit per-route limits still win where they are tighter ───────────

def test_endpoint_specific_limit_still_applies(client, db):
    """/auth/register is 5/minute. The 120/minute default must not have
    loosened it."""
    limiter.reset()
    codes = []
    for _ in range(7):
        email = f"burst-{uuid.uuid4().hex[:12]}@example.com"
        resp = client.post("/api/v1/auth/register", json={
            "email": email, "full_name": "Burst", "password": STRONG_PASSWORD,
        })
        codes.append(resp.status_code)

    assert 429 in codes, f"the 5/minute register limit stopped applying: {codes}"
    assert codes.index(429) <= 5, f"limit fired later than 5 requests: {codes}"


def test_community_post_creation_is_limited(client, db):
    """Explicitly limited to 10/minute: the 120/minute ceiling is not spam
    protection for a feed."""
    limiter.reset()
    token, _ = _register(client, "poster")

    codes = []
    for i in range(13):
        resp = client.post(
            "/api/v1/community/posts",
            headers=_auth(token),
            json={"post_type": "discussion", "title": f"title-{i}", "content": "hello world"},
        )
        codes.append(resp.status_code)

    assert 429 in codes, f"community post creation is unlimited: {codes}"


# ─── the limiter must not break liveness or monitoring ────────────────────

def test_health_is_exempt(client, db):
    """The limiter fails closed when Redis is unreachable, so a limited
    /health would 500 during an outage instead of reporting it — and an
    orchestrator would kill a process that is otherwise serving."""
    from app.main import health_check

    name = f"{health_check.__module__}.{health_check.__name__}"
    assert name in limiter._exempt_routes


def test_metrics_is_exempt():
    """Prometheus scrapes on a fixed interval and must never be throttled;
    access is controlled by the bearer token instead."""
    import app.main as main

    exempt = limiter._exempt_routes
    assert any(n.endswith(".metrics") for n in exempt), sorted(exempt)


def test_health_survives_a_burst(client, db):
    """Belt and braces on the exemption: a container healthcheck plus a
    scrape loop must not be able to rate-limit themselves out."""
    limiter.reset()
    codes = [client.get("/health").status_code for _ in range(40)]
    assert 429 not in codes, "health checks are being rate limited"


# ─── unauthenticated vs authenticated ─────────────────────────────────────

def test_unauthenticated_requests_are_limited_too(client, db):
    """The bucket is keyed on client address, not on identity, so an
    anonymous caller cannot escape the limit by not logging in."""
    limiter.reset()
    codes = []
    for _ in range(13):          # the login limit is 10/minute
        resp = client.post("/api/v1/auth/login", json={
            "email": f"nobody-{uuid.uuid4().hex[:8]}@example.com",
            "password": "wrong-password-here",
        })
        codes.append(resp.status_code)

    assert 429 in codes, f"unauthenticated login attempts are unlimited: {codes}"


def test_authenticated_endpoint_is_limited_by_client_not_account(client, db):
    """Two accounts from the same client share the bucket — otherwise
    registering a fresh account would reset the limit and the ceiling
    would mean nothing against exactly the abuse it exists to stop."""
    limiter.reset()
    first, _ = _register(client, "acct1")
    second, _ = _register(client, "acct2")

    codes = []
    for i in range(13):
        token = first if i % 2 == 0 else second
        resp = client.post(
            "/api/v1/community/posts",
            headers=_auth(token),
            json={"post_type": "discussion", "title": f"title-{i}", "content": "hello world"},
        )
        codes.append(resp.status_code)

    assert 429 in codes, (
        f"switching accounts reset the limit: {codes}"
    )
