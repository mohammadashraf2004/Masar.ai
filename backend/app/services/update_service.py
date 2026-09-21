"""Acknowledging product announcements (see app.core.releases)."""
from typing import Iterable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core import releases
from app.models.update_ack import UserUpdateAcknowledgement


def acknowledge(db: Session, user_id: int, release_id: str) -> None:
    """Record that the account has seen `release_id` (and what it covers).

    Idempotent: a repeat writes nothing, and two racing requests resolve to one
    row - the unique constraint is the arbiter, the SELECT is the fast path.
    The caller commits. Touches nothing else: not the roadmap, not the skills.
    """
    _record(db, user_id, releases.with_covered(release_id))


def _record(db: Session, user_id: int, release_ids: Iterable[str]) -> None:
    wanted = list(release_ids)
    have = {
        rid for (rid,) in db.query(UserUpdateAcknowledgement.release_id).filter(
            UserUpdateAcknowledgement.user_id == user_id,
            UserUpdateAcknowledgement.release_id.in_(wanted),
        )
    }
    for rid in wanted:
        if rid in have:
            continue
        try:
            with db.begin_nested():
                db.add(UserUpdateAcknowledgement(user_id=user_id, release_id=rid))
        except IntegrityError:
            pass  # a concurrent request recorded it first: the outcome is the same
