"""
Covers the Prometheus endpoint and the label discipline behind it.

The interesting failure modes here are quiet ones — metrics that are wrong
rather than absent — so these tests target the two that actually bit during
implementation:

  * route labels that drop the router prefix, so `/api/v1/auth/login` is
    recorded as `/auth/login` and collides with any other router sharing
    that suffix;
  * unbounded label values, where every URL a scanner tries mints a new
    time series until the scrape falls over.

And the one that matters for exposure: /metrics is served on the public
port, so a wrong token must not return the payload.
"""
import uuid

import pytest
from starlette.datastructures import URL

from app.core.config import settings
from app.core.metrics import route_template


class _FakeRequest:
    """Minimal stand-in: route_template only reads the scope and the path."""

    def __init__(self, path, route=object(), path_params=None):
        self.scope = {"route": route, "path_params": path_params or {}}
        self.url = URL(f"http://testserver{path}")


# ─── Label discipline ────────────────────────────────────────────────────


def test_route_template_keeps_the_router_prefix():
    """The bug this exists for: `scope["route"].path` is relative to its own
    router in this FastAPI version, which silently dropped `/api/v1`."""
    request = _FakeRequest("/api/v1/auth/login")
    assert route_template(request) == "/api/v1/auth/login"


def test_route_template_collapses_path_parameters():
    """Two different courses must be one time series, not two."""
    a = _FakeRequest("/api/v1/tool-courses/langchain", path_params={"slug": "langchain"})
    b = _FakeRequest("/api/v1/tool-courses/qdrant", path_params={"slug": "qdrant"})
    assert route_template(a) == route_template(b) == "/api/v1/tool-courses/{slug}"


def test_route_template_substitutes_per_segment():
    """A substring replace would rewrite whichever `1` came first; the id
    parameter is the second one here."""
    request = _FakeRequest(
        "/api/v1/exams/1/attempts/7",
        path_params={"attempt_id": 7},
    )
    assert route_template(request) == "/api/v1/exams/1/attempts/{attempt_id}"


def test_unmatched_requests_share_one_label():
    """Otherwise every URL a scanner tries becomes its own time series."""
    for path in ("/wp-admin", "/.env", "/api/v1/nope"):
        assert route_template(_FakeRequest(path, route=None)) == "unmatched"


# ─── Endpoint behaviour ──────────────────────────────────────────────────


@pytest.fixture()
def metrics_token(monkeypatch):
    token = f"test-token-{uuid.uuid4().hex}"
    monkeypatch.setattr(settings, "METRICS_TOKEN", token)
    return token


def test_metrics_requires_the_token(client, metrics_token):
    # 404, not 401: an unauthenticated caller should not learn the endpoint
    # exists at all.
    assert client.get("/metrics").status_code == 404
    assert client.get("/metrics", headers={"Authorization": "Bearer wrong"}).status_code == 404


def test_metrics_served_with_the_token(client, metrics_token):
    response = client.get("/metrics", headers={"Authorization": f"Bearer {metrics_token}"})
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "http_requests_total" in response.text


def test_metrics_accepts_the_token_as_a_query_parameter(client, metrics_token):
    """For scrapers that cannot set a header."""
    assert client.get("/metrics", params={"token": metrics_token}).status_code == 200


def test_requests_are_counted_under_their_route_template(client, metrics_token):
    """End to end through the middleware: two different slugs, one series.

    Checks the whole payload, not just the request counter — an early
    version labelled the in-flight gauge with the raw path, which put every
    URL back into the exposition one series at a time.
    """
    client.get("/api/v1/tool-courses/does-not-exist")
    client.get("/api/v1/tool-courses/also-missing")

    body = client.get("/metrics", headers={"Authorization": f"Bearer {metrics_token}"}).text

    assert 'path="/api/v1/tool-courses/{slug}"' in body
    assert "does-not-exist" not in body
    assert "also-missing" not in body


def test_health_endpoint_is_measured(client, metrics_token):
    client.get("/health")
    body = client.get("/metrics", headers={"Authorization": f"Bearer {metrics_token}"}).text
    assert 'http_requests_total{method="GET",path="/health"' in body
    assert "http_request_duration_seconds_bucket" in body


# ─── Business counters ───────────────────────────────────────────────────


def test_auth_events_are_counted(client, metrics_token):
    """security_log is the choke point every auth outcome passes through,
    so registering must move the counter without the controller knowing."""
    client.post("/api/v1/auth/register", json={
        "email": f"metrics-{uuid.uuid4().hex[:12]}@example.com",
        "full_name": "Metrics Probe",
        "password": "correcthorsebatterystaple",
    })

    body = client.get("/metrics", headers={"Authorization": f"Bearer {metrics_token}"}).text
    assert 'auth_events_total{event="register"}' in body


def test_metrics_carry_no_identifying_labels(client, metrics_token):
    """Counters are exposed on a port a scraper reaches; they must not carry
    anything that identifies a user, unlike the security log they sit next
    to."""
    email = f"metrics-{uuid.uuid4().hex[:12]}@example.com"
    client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Metrics Probe", "password": "correcthorsebatterystaple",
    })

    body = client.get("/metrics", headers={"Authorization": f"Bearer {metrics_token}"}).text
    assert email not in body
    assert "Metrics Probe" not in body
