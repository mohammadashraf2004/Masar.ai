"""
backend/app/core/login_guard.py

Per-account failed-login throttling, on top of the per-IP rate limit.

WHAT THIS DOES AND DOES NOT DEFEND AGAINST
------------------------------------------
The counter is keyed on (email, ip). That means:

  * It stops one source address grinding guesses against one account
    beyond LOGIN_MAX_FAILURES, even across a fleet of workers.

  * It does NOT, on its own, stop distributed credential stuffing —
    many source addresses each trying a few passwords against the same
    account get a fresh counter per address, by design. Keying on the
    email alone would stop that, but would also hand any attacker a
    trivial way to lock any user out of their own account by
    deliberately failing logins against it. That denial-of-service is
    the worse trade for a learning platform, so the pairing stands and
    cross-IP stuffing is addressed by the per-IP rate limit plus the
    `auth.login.locked` / `auth.login.failure` security events, which
    are what alerting should watch.

    (An earlier version of this docstring claimed the lockout applied
    "regardless of how many source addresses are used". That was wrong,
    and the security report has been corrected to match.)

STORAGE
-------
Counters live in the same backend as the rate limiter — Redis in
production (required, see app.core.config), in-process memory in
development and tests. Using process-local state here would make the
threshold per-worker: with gunicorn `-w 4` a configured limit of 8
would really admit up to 32 before engaging, and would reset on every
deploy. The shared backend keeps the configured number the real one.

The counting itself goes through `limits`' FixedWindowRateLimiter — the
same primitive slowapi uses — rather than raw Storage.incr(). Raw incr()
does not set a TTL on the Redis key, so lockout entries never expired
and a locked-out account stayed locked forever; and its return value
means different things on different backends. The strategy object
handles both correctly and identically on memory and Redis.
"""
import time
from typing import Optional

from limits import RateLimitItemPerSecond
from limits.strategies import FixedWindowRateLimiter

from app.core.config import settings
from app.core.limiter import limiter

_PREFIX = "loginguard"


def _window_seconds() -> int:
    return int(settings.LOGIN_LOCKOUT_MINUTES * 60)


def _item() -> RateLimitItemPerSecond:
    """Built per call so a settings change is picked up without a reimport."""
    return RateLimitItemPerSecond(settings.LOGIN_MAX_FAILURES, _window_seconds())


def _ids(email: str, ip: Optional[str]) -> tuple:
    return (_PREFIX, email, ip or "unknown")


def _strategy() -> FixedWindowRateLimiter:
    return FixedWindowRateLimiter(limiter._storage)


def seconds_until_unlocked(email: str, ip: Optional[str]) -> int:
    """0 when the caller may attempt a login; otherwise how long to wait."""
    try:
        stats = _strategy().get_window_stats(_item(), *_ids(email, ip))
    except Exception:
        # A storage blip must not become a login outage. The per-IP rate
        # limiter is configured to fail closed on the same backend, so a
        # genuine outage is already surfaced there rather than here.
        return 0
    if stats.remaining > 0:
        return 0
    # `remaining == 0` is the lock decision; reset_time only shapes the
    # Retry-After hint, and is floored at 1s so a lock is never reported
    # as "0 seconds to wait" (which the caller reads as unlocked).
    return max(1, int(stats.reset_time - time.time()))


def record_failure(email: str, ip: Optional[str]) -> int:
    """Returns the running failure count for this (email, ip)."""
    try:
        strategy, item = _strategy(), _item()
        # The window starts at the first failure and does not slide, so a
        # steady trickle of guesses cannot hold the entry alive forever.
        strategy.hit(item, *_ids(email, ip))
        stats = strategy.get_window_stats(item, *_ids(email, ip))
        return settings.LOGIN_MAX_FAILURES - stats.remaining
    except Exception:
        return 0


def record_success(email: str, ip: Optional[str]) -> None:
    """A correct password clears the counter for that pair."""
    try:
        _strategy().clear(_item(), *_ids(email, ip))
    except Exception:
        pass


def reset() -> None:
    """Test hook — mirrors limiter.reset()."""
    storage = limiter._storage
    if hasattr(storage, "reset"):
        try:
            storage.reset()
        except Exception:
            pass
