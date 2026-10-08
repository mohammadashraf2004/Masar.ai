"""The Pro plan's included AI usage: 50 credits per rolling 4 hours.

A Pro subscriber's AI actions (the ones that call the model provider, at the same
per-action prices the wallet uses) are paid from this allowance, never from the
wallet; when it is used up the request is refused before the provider is called,
and purchased or promotional wallet credits are not touched. Free accounts keep
paying from the wallet exactly as before. Course access never depends on it.

Accounting is a ledger (`pro_ai_usage`), one row per action:

* **reserved** before the provider call, under a per-account advisory lock, so
  concurrent requests can never together pass the limit;
* **consumed** when the request succeeds (`AllowanceRequestMiddleware`);
* **released** when the action failed and was refunded, or when nothing settled
  the reservation within `PRO_AI_RESERVATION_TTL_SECONDS` (a worker killed
  mid-request delivered nothing) - the credits are free again, and
  `release_reason` records why.

Consumed rows, and reservations still inside that lifetime, count for
`PRO_AI_WINDOW_SECONDS` from `reserved_at`:
the window rolls, nothing resets at a fixed hour, and credits come back one usage
at a time as each leaves the window. The window is per account, not per
subscription, so cancelling and resubscribing never refills it.
"""
from __future__ import annotations

import contextvars
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import and_, or_, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.billing import ProAiUsage, UserSubscription
from app.services.billing.subscriptions import PRO_PLAN_CODE, current_subscription, subscription_is_entitled

logger = logging.getLogger("app.billing.pro_ai")

# Actions that call the model provider. Everything else - reading, quizzes,
# deterministic exercises, challenge enrolment - never touches the allowance.
PRO_AI_ACTIONS = frozenset({
    "mentor_chat", "mentor_message", "code_review", "skill_gap", "mock_interview",
    "roadmap", "exercise_feedback", "project_hint", "challenge_hint",
})
_LOCK_NAMESPACE = 36036          # pg_advisory_xact_lock(namespace, user_id)
_COUNTED = ("reserved", "consumed")
UNSETTLED = "unsettled: the request never answered"


@dataclass(frozen=True)
class AllowanceStatus:
    limit: int
    window_seconds: int
    used: int
    remaining: int
    next_credit_available_at: Optional[datetime]

    def as_dict(self) -> dict:
        return {
            "limit": self.limit, "window_seconds": self.window_seconds, "used": self.used,
            "remaining": self.remaining,
            "next_credit_available_at": _iso(self.next_credit_available_at),
        }


class AllowanceExceeded(Exception):
    def __init__(self, status: AllowanceStatus, needed: int, available_at: Optional[datetime]):
        super().__init__("pro_ai_limit_reached")
        self.status, self.needed, self.available_at = status, needed, available_at


class DuplicateRequest(Exception):
    """The same request key already has a live (reserved or consumed) usage."""


def _iso(value: Optional[datetime]) -> Optional[str]:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if value else None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def eligible_subscription(db: Session, user_id: int, now: Optional[datetime] = None) -> Optional[UserSubscription]:
    """The server-verified subscription that carries the allowance, if any: an
    entitled Pro subscription (active, or cancelled but still inside its paid
    period), and a trial when PRO_AI_INCLUDE_TRIAL is on. Expired: none."""
    subscription = current_subscription(db, user_id)
    if not subscription_is_entitled(subscription, now):
        return None
    if subscription.status == "trialing" and not settings.PRO_AI_INCLUDE_TRIAL:
        return None
    return subscription if subscription.plan.code == PRO_PLAN_CODE else None


def _window_rows(db: Session, user_id: int, now: datetime) -> List[tuple]:
    since = now - timedelta(seconds=settings.PRO_AI_WINDOW_SECONDS)
    live = now - timedelta(seconds=settings.PRO_AI_RESERVATION_TTL_SECONDS)
    return db.query(ProAiUsage.reserved_at, ProAiUsage.credits).filter(
        ProAiUsage.user_id == user_id, ProAiUsage.reserved_at > since,
        or_(ProAiUsage.status == "consumed",
            and_(ProAiUsage.status == "reserved", ProAiUsage.reserved_at >= live)),
    ).order_by(ProAiUsage.reserved_at.asc(), ProAiUsage.id.asc()).all()


def _available_at(rows: List[tuple], remaining: int, needed: int) -> Optional[datetime]:
    """When `needed` credits will be free: walk the window's usages oldest first
    until enough of them have left it."""
    if remaining >= needed:
        return None
    window = timedelta(seconds=settings.PRO_AI_WINDOW_SECONDS)
    freed = remaining
    for reserved_at, credits in rows:
        freed += credits
        if freed >= needed:
            return _aware(reserved_at) + window
    return None


def allowance_status(db: Session, user_id: int, now: Optional[datetime] = None) -> AllowanceStatus:
    now = now or _now()
    rows = _window_rows(db, user_id, now)
    limit = settings.PRO_AI_CREDITS_PER_WINDOW
    used = sum(credits for _, credits in rows)
    remaining = max(0, limit - used)
    return AllowanceStatus(limit, settings.PRO_AI_WINDOW_SECONDS, used, remaining,
                           _available_at(rows, remaining, 1) if remaining == 0 else None)


def _release_stale(db: Session, user_id: int, now: datetime) -> None:
    """A reservation nobody settled in time belongs to a request that never
    answered: it delivered nothing, so its credits come back."""
    stale = now - timedelta(seconds=settings.PRO_AI_RESERVATION_TTL_SECONDS)
    db.query(ProAiUsage).filter(
        ProAiUsage.user_id == user_id, ProAiUsage.status == "reserved", ProAiUsage.reserved_at < stale,
    ).update({ProAiUsage.status: "released", ProAiUsage.released_at: now, ProAiUsage.release_reason: UNSETTLED},
             synchronize_session=False)


def reserve(
    db: Session, user_id: int, subscription: UserSubscription, action_type: str, credits: int,
    *, request_key: Optional[str] = None, now: Optional[datetime] = None,
) -> ProAiUsage:
    """Reserve `credits` from the allowance before calling the provider, or raise
    AllowanceExceeded (nothing reserved) / DuplicateRequest. Commits, so the
    reservation is durable - and the lock released - before the slow call."""
    now = now or _now()
    db.execute(text("SELECT pg_advisory_xact_lock(:ns, :uid)"), {"ns": _LOCK_NAMESPACE, "uid": user_id})
    _release_stale(db, user_id, now)
    previous = None
    if request_key:
        previous = db.query(ProAiUsage).filter(
            ProAiUsage.user_id == user_id, ProAiUsage.request_key == request_key,
        ).with_for_update().first()
        if previous is not None and previous.status in _COUNTED:
            db.rollback()
            raise DuplicateRequest(request_key)

    rows = _window_rows(db, user_id, now)
    limit = settings.PRO_AI_CREDITS_PER_WINDOW
    used = sum(c for _, c in rows)
    remaining = max(0, limit - used)
    if credits > remaining:
        status = AllowanceStatus(limit, settings.PRO_AI_WINDOW_SECONDS, used, remaining,
                                 _available_at(rows, remaining, 1) if remaining == 0 else None)
        available_at = _available_at(rows, remaining, credits) if credits <= limit else None
        db.rollback()
        raise AllowanceExceeded(status, credits, available_at)

    if previous is not None:          # a retry of a request whose earlier attempt was released
        previous.status, previous.credits, previous.action_type = "reserved", credits, action_type
        previous.reserved_at, previous.finalized_at, previous.released_at = now, None, None
        previous.release_reason = None
        previous.subscription_id = subscription.id
        usage = previous
    else:
        usage = ProAiUsage(user_id=user_id, subscription_id=subscription.id, action_type=action_type,
                           credits=credits, status="reserved", request_key=request_key, reserved_at=now)
        db.add(usage)
    try:
        db.commit()
    except IntegrityError:            # the same key raced in through another worker
        db.rollback()
        raise DuplicateRequest(request_key)
    return usage


def release(db: Session, usage_id: int, now: Optional[datetime] = None, reason: Optional[str] = None) -> bool:
    """Give a failed action's credits back. Idempotent: only a reservation that is
    still open is released."""
    released = db.execute(text(
        "UPDATE pro_ai_usage SET status = 'released', released_at = :now, release_reason = :reason "
        "WHERE id = :id AND status = 'reserved' RETURNING id"),
        {"id": usage_id, "now": now or _now(), "reason": (reason or "")[:120] or None}).first()
    db.commit()
    return released is not None


def released_since(db: Session, user_id: int, action_type: str, reason: str, since: datetime) -> int:
    """How many of this account's allowance charges for `action_type` were given
    back for `reason` since `since` - the allowance's half of a refund cap that is
    otherwise read from the wallet ledger (Mentor v2's validation refunds)."""
    return db.query(ProAiUsage.id).filter(
        ProAiUsage.user_id == user_id, ProAiUsage.action_type == action_type, ProAiUsage.status == "released",
        ProAiUsage.release_reason == reason[:120], ProAiUsage.released_at >= since,
    ).count()


def finalize(db: Session, usage_ids: List[int], now: Optional[datetime] = None) -> int:
    """Mark the reservations of a request that succeeded as consumed. Idempotent."""
    if not usage_ids:
        return 0
    done = db.execute(text(
        "UPDATE pro_ai_usage SET status = 'consumed', finalized_at = :now "
        "WHERE id = ANY(:ids) AND status = 'reserved' RETURNING id"), {"ids": list(usage_ids), "now": now or _now()}).all()
    db.commit()
    return len(done)


# ── Request scope ─────────────────────────────────────────────────────────────
# deduct_credits records each reservation here and refund_credits finds the one it
# must release, so a refund always gives back exactly the credits the same request
# took from the same place. AllowanceRequestMiddleware installs a fresh list per
# request (the list object is shared with the worker thread the endpoint runs on)
# and finalizes what is left when the response is a success.

@dataclass
class RequestCharge:
    user_id: int
    action_type: str
    credits: int
    usage_id: int
    released: bool = False


_request_charges: contextvars.ContextVar[Optional[list]] = contextvars.ContextVar("pro_ai_charges", default=None)
_request_key: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("pro_ai_request_key", default=None)


def begin_request(idempotency_key: Optional[str]) -> list:
    charges: list = []
    _request_charges.set(charges)
    _request_key.set(idempotency_key[:120] if idempotency_key else None)
    return charges


def current_request_key(action_type: str) -> Optional[str]:
    key = _request_key.get()
    return f"{action_type}:{key}" if key else None


def remember(charge: RequestCharge) -> None:
    charges = _request_charges.get()
    if charges is None:          # called outside an HTTP request (a job, a test)
        charges = []
        _request_charges.set(charges)
    charges.append(charge)


def take(user_id: int, action_type: str, credits: int) -> tuple[Optional[RequestCharge], bool]:
    """(charge, already_released): the most recent allowance charge of this request
    for this action that is still open - now marked released - or, when every such
    charge was already given back, (None, True), so a repeated refund is a no-op
    instead of crediting a wallet that was never charged."""
    matching = [c for c in (_request_charges.get() or [])
                if (c.user_id, c.action_type, c.credits) == (user_id, action_type, credits)]
    for charge in reversed(matching):
        if not charge.released:
            charge.released = True
            return charge, False
    return None, bool(matching)


def _settle_request(charges: List[RequestCharge], succeeded: bool) -> None:
    from app.db.session import SessionLocal

    open_charges = [c for c in charges if not c.released]
    if not open_charges:
        return
    db = SessionLocal()
    try:
        if succeeded:
            finalize(db, [c.usage_id for c in open_charges])
        else:
            for charge in open_charges:
                release(db, charge.usage_id, reason="request failed")
    except Exception:  # noqa: BLE001 - settling must never turn a response into a 500
        logger.exception("billing.pro_ai.settle_failed")
        db.rollback()
    finally:
        db.close()


class AllowanceRequestMiddleware:
    """Gives every HTTP request its own allowance-charge list and settles what is
    left in it once the response status is known: a 2xx/3xx consumes the
    reservations, anything else (including an unhandled exception) releases them.
    An `Idempotency-Key` request header names the request, so a replayed key
    cannot reserve a second time while the first is live."""

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        key = next((v for k, v in scope.get("headers") or [] if k == b"idempotency-key"), None)
        charges = begin_request(key.decode("latin-1") if key else None)
        outcome = {"status": 500}

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                outcome["status"] = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            if charges:
                from starlette.concurrency import run_in_threadpool

                await run_in_threadpool(_settle_request, list(charges), 200 <= outcome["status"] < 400)
