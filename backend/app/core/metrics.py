"""
backend/app/core/metrics.py

Prometheus instrumentation.

**Why the multiprocess dance.** The api container runs gunicorn with four
uvicorn workers, and prometheus_client's default registry lives in process
memory. Scraping a port that round-robins across four processes would return
whichever worker happened to answer — counters would appear to jump backwards
on every scrape and no rate() over them would mean anything. So the workers
write to a shared directory (`PROMETHEUS_MULTIPROC_DIR`) and `/metrics`
aggregates across all of them at scrape time. `gunicorn.conf.py` cleans a
worker's files when it dies; without that, a restarted worker's counters
would be double-counted forever.

Set `PROMETHEUS_MULTIPROC_DIR` and this is automatic. Leave it unset — a
single uvicorn in local dev, or the test suite — and the ordinary in-process
registry is used instead.

**What is instrumented.** HTTP is automatic via the middleware. Everything
else is deliberately narrow: one call site each at the places where money,
trust or capacity is actually spent — the LLM providers, credit deduction,
auth outcomes, payments, rate limiting. That is roughly six lines scattered
across the codebase rather than an instrumentation layer to maintain.

**Cardinality.** Labels only ever take values from a fixed set: route
*templates* (never raw paths), HTTP methods, status codes, provider and model
names, action names. A request to an unrouted URL is labelled `unmatched`, so
a scanner walking random paths cannot mint a new time series per request.
"""
from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from typing import Iterator, Optional

# ── Must run BEFORE prometheus_client is imported ────────────────────────
# prometheus_client decides in-process vs multiprocess mode exactly once, at
# import time, in values.get_value_class() — and it decides on the *presence*
# of the key, not its value:
#
#     if 'PROMETHEUS_MULTIPROC_DIR' in os.environ: return MultiProcessValue()
#
# So `PROMETHEUS_MULTIPROC_DIR=""` — which docker-compose.dev.yml sets
# because Compose cannot unset an inherited variable — switched multiprocess
# mode ON, not off. The path was then built as
# `os.path.join("", "counter_<pid>.db")`, which is relative, so every worker
# wrote its mmap files into the process's working directory: /app, i.e. the
# bind-mounted source tree. That left hundreds of counter_*.db /
# gauge_livesum_*.db / histogram_*.db files sitting in backend/, three more
# per reload, none of them ever retired.
#
# It was also silently wrong in a second way: multiprocess_enabled() below
# tests truthiness, so it reported "off" and render_metrics() served the
# in-process registry while the values were being written to files nobody
# read.
#
# Deleting the key is the only way to say "off", because that is the only
# thing the library looks at.
MULTIPROC_ENV = "PROMETHEUS_MULTIPROC_DIR"
_LEGACY_MULTIPROC_ENV = "prometheus_multiproc_dir"  # pre-0.12 spelling, still honoured


def _sanitize_multiproc_env() -> None:
    for key in (MULTIPROC_ENV, _LEGACY_MULTIPROC_ENV):
        value = os.environ.get(key)
        if value is None:
            continue
        if not value.strip():
            # Blank means "the operator wanted this off". Honour that.
            del os.environ[key]
        elif not os.path.isabs(value):
            # Same footgun, one step removed: a relative path is resolved
            # against the working directory, which for this app is the
            # source tree. Loud rather than silently corrected — someone
            # chose this value and a wrong metrics directory is better
            # discovered than papered over.
            logging.getLogger(__name__).warning(
                "%s=%r is a relative path; metric files will be written under "
                "the working directory (%s). Use an absolute path.",
                key, value, os.getcwd(),
            )


_sanitize_multiproc_env()

from prometheus_client import (  # noqa: E402 — must follow the sanitiser above
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    multiprocess,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


def multiprocess_enabled() -> bool:
    return bool(os.environ.get(MULTIPROC_ENV))


def _ensure_multiproc_dir() -> None:
    """Create the shared directory if it is missing.

    Failure here is silent in a way that wastes an afternoon: if the
    directory does not exist, prometheus_client still imports, the app still
    serves, and /metrics returns an empty body — no error, no warning, just
    no metrics. gunicorn.conf.py creates it in the master process, but this
    covers every other way the app can start (a single uvicorn, a one-off
    container, a typo'd mount path).
    """
    directory = os.environ.get(MULTIPROC_ENV)
    if not directory:
        return
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        logging.getLogger(__name__).warning(
            "PROMETHEUS_MULTIPROC_DIR=%s is not creatable; /metrics will be empty",
            directory,
        )


_ensure_multiproc_dir()


# ─── HTTP ────────────────────────────────────────────────────────────────

http_requests_total = Counter(
    "http_requests_total",
    "HTTP requests by route template, method and status class.",
    ["method", "path", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency.",
    ["method", "path"],
    # Tuned for this app: most routes are a couple of database queries, but
    # the AI ones legitimately take seconds, and the difference between 5s
    # and 30s is the difference between slow and abandoned.
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30, 60),
)

http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "Requests currently being served.",
    # Labelled by method only, deliberately. This gauge has to be
    # incremented *before* routing, when the only path available is the raw
    # one — and labelling by raw path is precisely the unbounded-cardinality
    # bug the route templates exist to avoid: one series per URL a scanner
    # tries, forever. "How many requests are in flight" is the question this
    # answers; per-route concurrency is not worth that cost.
    ["method"],
    # Across workers this must be a sum of live processes, not a max or a
    # stale leftover from a worker that has since exited.
    multiprocess_mode="livesum",
)

http_exceptions_total = Counter(
    "http_exceptions_total",
    "Requests that raised out of the handler.",
    ["path", "exception"],
)

# ─── LLM spend and latency ───────────────────────────────────────────────

llm_requests_total = Counter(
    "llm_requests_total",
    "Calls to an LLM provider.",
    ["provider", "model", "outcome"],
)

llm_request_duration_seconds = Histogram(
    "llm_request_duration_seconds",
    "LLM call latency.",
    ["provider", "model"],
    buckets=(0.5, 1, 2.5, 5, 10, 20, 30, 60, 120),
)

llm_tokens_total = Counter(
    "llm_tokens_total",
    "Tokens billed by an LLM provider, by direction.",
    ["provider", "model", "direction"],
)

# ─── Product and money ───────────────────────────────────────────────────

credits_spent_total = Counter(
    "credits_spent_total",
    "Credits deducted from user wallets, by action.",
    ["action"],
)

credit_denials_total = Counter(
    "credit_denials_total",
    "AI actions refused because the wallet could not cover them.",
    ["action"],
)

auth_events_total = Counter(
    "auth_events_total",
    "Authentication outcomes.",
    ["event"],
)

payments_total = Counter(
    "payments_total",
    "Payment lifecycle events.",
    ["kind", "status"],
)

rate_limit_hits_total = Counter(
    "rate_limit_hits_total",
    "Requests rejected by a rate limit.",
    ["path"],
)


# ─── Recording helpers ───────────────────────────────────────────────────
# Thin wrappers so call sites never import prometheus_client directly, and
# so a metrics failure can never take down the request it was measuring.


class _LLMCall:
    """Handle yielded by `observe_llm_call` for reporting token usage."""

    def __init__(self) -> None:
        self.input_tokens = 0
        self.output_tokens = 0

    def record_usage(self, input_tokens: Optional[int], output_tokens: Optional[int]) -> None:
        self.input_tokens = int(input_tokens or 0)
        self.output_tokens = int(output_tokens or 0)


@contextmanager
def observe_llm_call(provider: str, model: str) -> Iterator[_LLMCall]:
    """Time one provider call, and record its token usage and outcome.

    Token counts are the pre-launch question that matters most — "what is
    this costing per user" — and they are only available from the provider's
    own response, which is why the call sites report them rather than the
    middleware inferring anything.
    """
    call = _LLMCall()
    started = time.perf_counter()
    outcome = "error"
    try:
        yield call
        outcome = "success"
    finally:
        elapsed = time.perf_counter() - started
        try:
            llm_request_duration_seconds.labels(provider, model).observe(elapsed)
            llm_requests_total.labels(provider, model, outcome).inc()
            if call.input_tokens:
                llm_tokens_total.labels(provider, model, "input").inc(call.input_tokens)
            if call.output_tokens:
                llm_tokens_total.labels(provider, model, "output").inc(call.output_tokens)
        except Exception:  # noqa: BLE001 — telemetry must never break a call
            pass


def record_credits_spent(action: str, credits: int) -> None:
    try:
        credits_spent_total.labels(action).inc(credits)
    except Exception:  # noqa: BLE001
        pass


def record_credit_denial(action: str) -> None:
    try:
        credit_denials_total.labels(action).inc()
    except Exception:  # noqa: BLE001
        pass


def record_auth_event(event: str) -> None:
    try:
        auth_events_total.labels(event).inc()
    except Exception:  # noqa: BLE001
        pass


def record_payment(kind: str, status: str) -> None:
    try:
        payments_total.labels(kind, status).inc()
    except Exception:  # noqa: BLE001
        pass


def record_rate_limit_hit(path: str) -> None:
    try:
        rate_limit_hits_total.labels(path).inc()
    except Exception:  # noqa: BLE001
        pass


# ─── Middleware ──────────────────────────────────────────────────────────


def route_template(request: Request) -> str:
    """The matched route's template, e.g. `/api/v1/tracks/{slug}`.

    Never the raw path: `/api/v1/tracks/langchain` and `/api/v1/tracks/qdrant`
    are the same endpoint, and labelling them separately would mint a new
    time series per slug — and per garbage path a scanner tries.

    Built by substituting the matched path parameters back into the request
    path, rather than reading `scope["route"].path`. This FastAPI version
    nests included routers instead of flattening them, so the route object
    in the scope carries its path *relative to its own router* — the label
    came out as `/auth/login`, silently dropping the `/api/v1` prefix and
    colliding with any other router that happened to use the same suffix.
    Substitution is prefix-agnostic and survives however the routers are
    composed.
    """
    if request.scope.get("route") is None:
        # Nothing matched: a 404 from a scanner walking random URLs. One
        # bucket for all of it — this is the label that would otherwise grow
        # without limit.
        return "unmatched"

    params = request.scope.get("path_params") or {}
    path = request.url.path
    if not params:
        return path

    # Segment-wise, not a substring replace: in `/exams/1/attempts/1` a
    # substring replace would rewrite whichever `1` came first, which is not
    # necessarily the parameter.
    placeholders = {str(value): "{" + name + "}" for name, value in params.items()}
    return "/".join(placeholders.get(segment, segment) for segment in path.split("/"))


class MetricsMiddleware(BaseHTTPMiddleware):
    """Times every request and records it against its route template."""

    async def dispatch(self, request: Request, call_next):
        method = request.method
        http_requests_in_progress.labels(method).inc()
        started = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = time.perf_counter() - started
            path = route_template(request)
            http_exceptions_total.labels(path, type(exc).__name__).inc()
            http_request_duration_seconds.labels(method, path).observe(elapsed)
            http_requests_total.labels(method, path, "500").inc()
            raise
        finally:
            http_requests_in_progress.labels(method).dec()

        elapsed = time.perf_counter() - started
        path = route_template(request)
        http_request_duration_seconds.labels(method, path).observe(elapsed)
        http_requests_total.labels(method, path, str(response.status_code)).inc()
        return response


# ─── Exposition ──────────────────────────────────────────────────────────


def render_metrics() -> Response:
    """The `/metrics` payload, aggregated across gunicorn workers."""
    if multiprocess_enabled():
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
    else:
        from prometheus_client import REGISTRY as registry  # type: ignore[assignment]

    return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
