"""One charge and one provider call per mentor request id, even when the request is repeated
while it is still running.

A send can be repeated by a timed-out browser, a dropped connection or a double click. The
client gives every user-triggered request an id and repeats it on a retry. The server claims
that id in `mentor_requests` before anything is charged:

* the first request inserts the row (`processing`); only it may charge and call the provider;
* a duplicate that arrives while it runs locks the same row, sees `processing` and gets a 409
  `request_in_progress` - no charge, no provider call - and retries later with the same id;
* a duplicate that arrives after it finished gets the stored response, free;
* after a failure (the owner refunded and marked the row `failed`) the same id may run again;
* a row left `processing` by a worker that died is taken over after STALE_AFTER, and a wallet
  charge it never gave back is refunded first.

The unique (user, action, request id) constraint is what makes this race-free: two inserts of
the same id cannot both succeed, and the row lock orders everything that follows. A request
without an id is not protected and behaves as before.
"""
from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterator, Optional

from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.mentor_request import MentorRequest

logger = logging.getLogger(__name__)

# Longer than any request can run (provider calls are budgeted to finish well inside a minute),
# so a row this old is a request whose worker is gone, not one still working.
STALE_AFTER = timedelta(seconds=120)
RETRY_AFTER_SECONDS = 3
# A retry comes within minutes. Finished claims older than this are deleted (the learner's own,
# on their next claim), so the table does not keep every reply forever. A row still `processing`
# is kept whatever its age: it records a charge that was never given back.
KEEP_FINISHED = timedelta(days=1)


@dataclass
class Claim:
    """`row` is the claim this request owns (None without a request id, or for a replay);
    `replay` is the stored response of a request that already finished."""
    row: Optional[MentorRequest] = None
    replay: Optional[Dict[str, Any]] = None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def in_progress() -> HTTPException:
    return HTTPException(
        status_code=409,
        detail={
            "error": "request_in_progress",
            "message": "This request is still being answered. It was not charged again.",
            "retry_after": RETRY_AFTER_SECONDS,
        },
        headers={"Retry-After": str(RETRY_AFTER_SECONDS)},
    )


def refund_abandoned(db: Session, user_id: int, now: Optional[datetime] = None) -> int:
    """Give back every wallet charge this learner's dead requests still hold; returns how many.

    A worker killed mid-request (a deploy, a crash, the host stalling) leaves its claim
    `processing` with the charge recorded. A retry of that same id refunds it (see claim), but a
    learner who never retries would never get it back. So any later claim of theirs settles
    them all. Rows are locked (SKIP LOCKED) and cleared in the same transaction that reads what
    they owe, so two requests at once cannot both refund one. A Pro reservation is not handled
    here: an unsettled one is released on its own (pro_ai_allowance)."""
    from app.services.wallet.wallet_service import refund_credits

    now = now or _now()
    rows = (
        db.query(MentorRequest)
        .filter(MentorRequest.user_id == user_id, MentorRequest.status == "processing",
                MentorRequest.updated_at < now - STALE_AFTER, MentorRequest.charged_credits > 0,
                MentorRequest.charge_source == "wallet")
        .with_for_update(skip_locked=True)
        .all()
    )
    owed = [(row.action, row.charged_credits) for row in rows]
    for row in rows:
        row.status, row.charged_credits, row.charge_source, row.updated_at = "failed", 0, None, now
    db.commit()
    for action, credits in owed:
        try:
            refund_credits(user_id, action, db, reason=f"Refund: {action} never answered", cost=credits)
        except Exception:
            logger.critical("%s abandoned-request refund FAILED; user is owed credits", action,
                            extra={"user_id": user_id, "action": action})
    return len(owed)


def claim(db: Session, user_id: int, action: str, request_id: Optional[str]) -> Claim:
    """Claim `request_id` for this request, or say what to do instead (see the module doc).
    Commits. Call it after the request is validated and before anything is charged."""
    if not request_id:
        return Claim()
    now = _now()
    refund_abandoned(db, user_id, now)
    db.query(MentorRequest).filter(
        MentorRequest.user_id == user_id, MentorRequest.status != "processing",
        MentorRequest.updated_at < now - KEEP_FINISHED,
    ).delete(synchronize_session=False)
    inserted = db.execute(
        insert(MentorRequest)
        .values(user_id=user_id, action=action, request_id=request_id, status="processing",
                created_at=now, updated_at=now)
        .on_conflict_do_nothing(constraint="uq_mentor_requests_user_action_request")
        .returning(MentorRequest.id)
    ).scalar()
    db.commit()
    if inserted is not None:
        return Claim(row=db.get(MentorRequest, inserted))

    row = (
        db.query(MentorRequest)
        .filter(MentorRequest.user_id == user_id, MentorRequest.action == action,
                MentorRequest.request_id == request_id)
        .with_for_update()
        .one()
    )
    if row.status == "done":
        replay = row.response
        db.commit()
        return Claim(replay=replay or {})
    if row.status == "processing" and now - _aware(row.updated_at) <= STALE_AFTER:
        db.rollback()
        raise in_progress()

    # Failed (refunded), or abandoned by a dead worker: this request takes it over.
    owed = row.charged_credits if row.charge_source == "wallet" else 0
    row.status, row.updated_at, row.response = "processing", now, None
    row.charged_credits, row.charge_source = 0, None
    db.commit()
    if owed:
        # Charged and never given back (the worker died, or its refund failed). A Pro
        # reservation needs nothing here: an unsettled reservation is released on its own.
        from app.services.wallet.wallet_service import refund_credits

        try:
            refund_credits(user_id, action, db, reason=f"Refund: {action} never answered", cost=owed)
        except Exception:
            logger.critical("%s abandoned-request refund FAILED; user is owed credits", action,
                            extra={"user_id": user_id, "action": action})
    return Claim(row=row)


def charged(db: Session, claim: Claim, charge: Dict[str, Any]) -> None:
    """Record what deduct_credits just took for the claimed request."""
    if claim.row is None:
        return
    claim.row.charged_credits = int(charge.get("credits_used") or 0)
    claim.row.charge_source = "pro" if charge.get("source") == "pro_allowance" else "wallet"
    claim.row.updated_at = _now()
    db.commit()


def refunded(db: Session, claim: Claim) -> None:
    """The claimed request's charge was given back."""
    if claim.row is None:
        return
    claim.row.charged_credits, claim.row.charge_source = 0, None
    db.commit()


def done(db: Session, claim: Claim, response: Dict[str, Any]) -> None:
    """Store the answer a repeat of this request id gets back."""
    if claim.row is None:
        return
    claim.row.status, claim.row.response, claim.row.updated_at = "done", response, _now()
    db.commit()


def failed(db: Session, claim: Claim) -> None:
    """The claimed request ended without an answer: the same id may run again. What it charged
    and did not give back stays recorded, so the next claim refunds it."""
    if claim.row is None:
        return
    row_id = claim.row.id
    try:
        db.rollback()
        db.query(MentorRequest).filter(MentorRequest.id == row_id, MentorRequest.status == "processing").update(
            {"status": "failed", "updated_at": _now()}, synchronize_session=False,
        )
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("could not mark mentor request %s failed", row_id)


@contextmanager
def guard(db: Session, claim: Claim) -> Iterator[None]:
    """Mark the claim failed if the work inside raises (a 402, a 503, anything)."""
    try:
        yield
    except BaseException:
        failed(db, claim)
        raise
