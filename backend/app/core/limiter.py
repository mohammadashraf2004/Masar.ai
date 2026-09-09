"""
Shared slowapi Limiter instance.

Lives in its own module (not app.main) so controllers can import it
without creating a circular import with app.main, which imports the
controllers to register their routers.

Two things here decide whether the documented rate limits are real:

1. WHERE the counters live. In-memory counters are per-process, and
   docker-compose runs gunicorn with `-w 4`, so a "10/minute" limit would
   actually admit 40/minute. Production requires REDIS_URL (enforced in
   app.core.config) and this module verifies the connection at import, so
   a missing or unreachable Redis is a startup failure rather than a
   silent downgrade.

2. WHAT the counters are keyed on. See client_key below.
"""
import ipaddress

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


def _peer_is_trusted_proxy(request) -> bool:
    """True only when the TCP peer is one of our configured proxies.

    This is what makes X-Forwarded-For trustworthy at all. Counting
    proxies alone assumes every request arrived through the proxy; this
    verifies it. A request that reaches the app port directly comes from
    an untrusted address, so its header is ignored no matter what it says.
    """
    nets = settings.trusted_proxy_networks
    if not nets:
        return False
    client = getattr(request, "client", None)
    host = getattr(client, "host", None)
    if not host:
        return False
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(addr in net for net in nets)


def client_key(request) -> str:
    """Client identity for rate-limit bucketing.

    X-Forwarded-For is an ordinary request header: anything that can open
    a socket can set it to any value. It is only meaningful when a proxy
    we control has appended to it, and only the entries that proxy (and
    proxies behind it) appended can be trusted — everything to their left
    was supplied by the caller.

    Proxies APPEND, so the chain grows left-to-right:

        client sends:            XFF: <anything the client likes>
        our edge proxy appends:  XFF: <client's junk>, <real client IP>
        a second proxy appends:  XFF: <client's junk>, <real IP>, <edge>

    With N trusted proxies the real client is therefore the Nth entry
    counting from the RIGHT — index -N — and every attacker-controlled
    value sits to the left of it, where we never look.

    The header is only consulted when BOTH hold:
      * TRUSTED_PROXY_COUNT > 0, and
      * the TCP peer is inside TRUSTED_PROXY_IPS.
    The second condition is what stops a client that can reach this port
    directly from sending a one-entry header that satisfies the count.

    With TRUSTED_PROXY_COUNT = 0 (the default, and correct for this
    repository, which publishes the API directly with no proxy in front)
    the header is ignored completely and the TCP peer address is used.

    An earlier version of this function read the LEFT-most entry whenever
    APP_ENV was production. That is the attacker-controlled position: one
    host could rotate the header to get a fresh bucket per request,
    bypassing the login/registration/password-reset limits and — because
    app.core.login_guard keys on (email, ip) — the per-account lockout as
    well.
    """
    n = settings.TRUSTED_PROXY_COUNT
    if n > 0 and _peer_is_trusted_proxy(request):
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            chain = [p.strip() for p in forwarded.split(",") if p.strip()]
            # Too short means the request did not traverse the expected
            # chain (someone hit an internal port directly, or a proxy is
            # misconfigured). Fall through to the peer address rather than
            # reading an entry the client could have planted.
            if len(chain) >= n:
                return chain[-n]
    return get_remote_address(request)


def _storage_uri() -> str:
    """Redis in production (required), in-memory elsewhere."""
    if settings.REDIS_URL:
        return settings.REDIS_URL
    if settings.is_production:
        # Defence in depth: app.core.config already refuses to construct
        # settings in this state, so reaching here means that check was
        # edited away. Fail loudly rather than quietly returning memory://.
        raise RuntimeError(
            "REDIS_URL is required in production — refusing to fall back to "
            "per-process in-memory rate limiting."
        )
    return "memory://"


# Backstop for every route that does NOT carry an explicit
# @limiter.limit(...). Before this, an endpoint without a decorator was
# simply unlimited — which covered every write endpoint in the community,
# exam, wallet, exam-payment and tool-course controllers, so post/comment
# spam had no ceiling at all.
#
# Two properties of slowapi 0.1.9 decide what this number can safely be,
# both verified against the installed source rather than assumed:
#
#   1. The bucket is per (client, endpoint), not global. __evaluate_limits
#      scopes each hit to `lim.scope or endpoint`, and the endpoint key is
#      the view function. So this is "120/minute to each individual route",
#      not "120/minute across the whole API" — one busy screen cannot
#      exhaust another screen's budget.
#   2. Defaults STACK with route decorators rather than being replaced by
#      them. In the middleware pass _check_request_limit leaves route_limits
#      empty, so `combined_defaults` is vacuously True and the default is
#      always appended. The effective limit on a decorated route is
#      therefore min(default, decorated).
#
# (2) is why this is 120 and not something tighter: 120/minute is the
# loosest explicit limit in the app (the Paymob webhook), so this value
# leaves every existing deliberate limit exactly as it was. Lowering it
# would silently tighten that webhook and start dropping payment
# confirmations under retry bursts.
#
# It is a ceiling, not a policy. Anything that needs a real limit should
# still say so explicitly on the route.
DEFAULT_LIMITS = ["120/minute"]

limiter = Limiter(
    key_func=client_key,
    storage_uri=_storage_uri(),
    default_limits=DEFAULT_LIMITS,
    # Fail closed if Redis goes away mid-flight: better to reject a
    # request than to silently stop rate-limiting the login endpoint.
    swallow_errors=False,
)


def verify_storage_reachable() -> None:
    """Probe the rate-limit backend so an unreachable Redis is a startup
    failure, not a surprise on the first login attempt. Called from
    app.main at import time; a no-op for in-memory storage.

    Note `limits`' Storage.check() signals failure by RETURNING False, not
    by raising — an earlier version of this function only caught
    exceptions and therefore let the app boot happily against a dead
    Redis, which is precisely the silent-degradation this is meant to
    prevent. Both outcomes are treated as failure here.
    """
    if not settings.REDIS_URL:
        return
    try:
        healthy = limiter._storage.check()
    except Exception as exc:
        raise RuntimeError(
            f"Rate-limit backend at REDIS_URL is unreachable ({exc.__class__.__name__}). "
            "Refusing to start: rate limits and login lockouts would not be enforced."
        ) from exc
    if not healthy:
        raise RuntimeError(
            "Rate-limit backend at REDIS_URL failed its health check. "
            "Refusing to start: rate limits and login lockouts would not be enforced."
        )
