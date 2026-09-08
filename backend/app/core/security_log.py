"""
backend/app/core/security_log.py

A single, deliberately narrow channel for security-relevant events:
authentication outcomes, privilege use, authorization failures, payment
confirmations, account lifecycle.

Everything here goes to the "security" logger so it can be shipped to a
SIEM / alerting pipeline separately from ordinary application chatter.

What must NEVER be passed to these functions: passwords, password hashes,
access tokens, refresh tokens, email-verification or password-reset
tokens, API keys, or full request bodies. Emails are recorded in
truncated, non-reversible form (see `mask_email`) so an operator can
correlate events without the log itself becoming a subscriber list. If a
new call site needs the raw address to be actionable, log the user id
instead — it's already the join key for everything else.
"""
import logging
from typing import Any, Optional

from app.core.metrics import record_auth_event, record_payment

logger = logging.getLogger("security")

# Successful, unremarkable events (a login that worked) are INFO; anything
# an operator might need to act on is WARNING.
EVENT_INFO = logging.INFO
EVENT_WARNING = logging.WARNING


def mask_email(email: Optional[str]) -> str:
    """a.student@example.com -> 'a***@example.com'. Enough to correlate
    repeated attempts against one account and to recognise an address you
    already know, without writing harvestable addresses to disk."""
    if not email or "@" not in email:
        return "<none>"
    local, _, domain = email.partition("@")
    head = local[0] if local else "?"
    return f"{head}***@{domain}"


def _emit(level: int, event: str, **fields: Any) -> None:
    parts = " ".join(f"{k}={v}" for k, v in fields.items() if v is not None)
    logger.log(level, "event=%s %s", event, parts)


# These functions are already the single choke point every auth and payment
# outcome passes through, which makes them the right place to count as well
# as log — no controller has to remember to do both. Counters carry no
# identity: an event name and nothing else, so the metric stays safe to
# expose where the log would not be.


def auth_success(*, user_id: int, email: str, ip: Optional[str]) -> None:
    _emit(EVENT_INFO, "auth.login.success", user_id=user_id, email=mask_email(email), ip=ip)
    record_auth_event("login.success")


def auth_failure(*, email: str, ip: Optional[str], reason: str) -> None:
    _emit(EVENT_WARNING, "auth.login.failure", email=mask_email(email), ip=ip, reason=reason)
    record_auth_event("login.failure")


def auth_lockout(*, email: str, ip: Optional[str], failures: int) -> None:
    _emit(EVENT_WARNING, "auth.login.locked", email=mask_email(email), ip=ip, failures=failures)
    record_auth_event("login.locked")


def registration(*, user_id: int, email: str, ip: Optional[str]) -> None:
    _emit(EVENT_INFO, "auth.register", user_id=user_id, email=mask_email(email), ip=ip)
    record_auth_event("register")


def password_reset_requested(*, email: str, ip: Optional[str], account_exists: bool) -> None:
    # account_exists stays server-side only — the HTTP response is
    # identical either way (see forgot_password).
    _emit(EVENT_INFO, "auth.password_reset.requested",
          email=mask_email(email), ip=ip, account_exists=account_exists)


def password_changed(*, user_id: int, via: str, ip: Optional[str]) -> None:
    _emit(EVENT_WARNING, "auth.password.changed", user_id=user_id, via=via, ip=ip)


def email_verified(*, user_id: int, ip: Optional[str]) -> None:
    _emit(EVENT_INFO, "auth.email.verified", user_id=user_id, ip=ip)
    record_auth_event("email.verified")


def token_consume_failed(*, purpose: str, ip: Optional[str], reason: str) -> None:
    _emit(EVENT_WARNING, "auth.token.rejected", purpose=purpose, ip=ip, reason=reason)


def sessions_revoked(*, user_id: int, via: str) -> None:
    _emit(EVENT_WARNING, "auth.sessions.revoked", user_id=user_id, via=via)


def account_deleted(*, user_id: int) -> None:
    _emit(EVENT_WARNING, "account.deleted", user_id=user_id)


def authz_denied(*, user_id: Optional[int], path: str, reason: str) -> None:
    _emit(EVENT_WARNING, "authz.denied", user_id=user_id, path=path, reason=reason)


def admin_action(*, admin_id: int, action: str, target: Any = None) -> None:
    _emit(EVENT_WARNING, "admin.action", admin_id=admin_id, action=action, target=target)


def payment_event(*, kind: str, ref: str, success: bool, user_id: Optional[int] = None) -> None:
    _emit(EVENT_INFO, "payment.webhook", kind=kind, ref=ref, success=success, user_id=user_id)
    record_payment(kind, "confirmed" if success else "failed")


def rate_limit_hit(*, path: str, ip: Optional[str]) -> None:
    _emit(EVENT_WARNING, "ratelimit.exceeded", path=path, ip=ip)


def server_error(*, error_id: str, path: str, method: str) -> None:
    """The public 500 response carries only `error_id`; the traceback and
    this line are the server-side half of that pair."""
    _emit(EVENT_WARNING, "app.error", error_id=error_id, path=path, method=method)
