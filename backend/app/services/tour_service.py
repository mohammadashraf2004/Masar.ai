"""Per-account walkthrough (tour) progress — see frontend/src/features/tours/ and
docs/backend-requests.md §6."""
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_tour import TourRecordStatus, UserTour

# Mirrors the frontend's TourId union (frontend/src/features/tours/registry.ts).
# Free-form on that side by design, but the server still refuses to store a
# tour_id it does not recognise — the same "unknown announcement" refusal as
# app.services.update_service — so a typo or a probe cannot create rows forever.
KNOWN_TOUR_IDS = {"onboarding", "mentor-interview", "language"}


def list_records(db: Session, user_id: int) -> List[UserTour]:
    return db.query(UserTour).filter(UserTour.user_id == user_id).all()


def get_record(db: Session, user_id: int, tour_id: str) -> Optional[UserTour]:
    return db.query(UserTour).filter(
        UserTour.user_id == user_id, UserTour.tour_id == tour_id,
    ).first()


def upsert(
    db: Session, user_id: int, tour_id: str,
    status: TourRecordStatus, version: int, at: Optional[datetime],
) -> UserTour:
    """Upsert a tour record, last-write-wins by `at`.

    `at` is the moment the status became true on the client, not the request's
    arrival time: a write queued while offline (or retried after a failure) can
    reach the server after a newer write from the same account already landed.
    An incoming `at` older than the stored one is exactly that race, and is a
    no-op — the caller gets the current row back unchanged, not an error, so a
    stale tab replaying its queue never has to know it lost the race.

    A missing `at` (no local clock to trust) uses the server's own time, which
    is always the newest possible value and so is never rejected as stale.
    """
    now = datetime.now(timezone.utc)
    when = at if at is not None else now
    if when.tzinfo is None:
        # A client timestamp without an offset is read as UTC; comparing it
        # raw with the stored timestamptz would raise.
        when = when.replace(tzinfo=timezone.utc)
    # A client clock cannot claim the future: a far-future `at` would
    # otherwise make every later (real) write look stale forever.
    when = min(when, now)
    existing = get_record(db, user_id, tour_id)
    if existing is not None:
        # A stored `at` in the future (a row written before client clocks were
        # clamped) is untrusted, so it never makes a real write look stale.
        stored = existing.at.replace(tzinfo=timezone.utc) if existing.at and existing.at.tzinfo is None else existing.at
        if stored is not None and stored <= now and when < stored:
            return existing
        existing.status = status
        existing.version = version
        existing.at = when
        db.commit()
        db.refresh(existing)
        return existing

    row = UserTour(user_id=user_id, tour_id=tour_id, status=status, version=version, at=when)
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        # A concurrent request inserted the same (user, tour) row first: the
        # same race `update_service.acknowledge` resolves — retry as an update.
        db.rollback()
        return upsert(db, user_id, tour_id, status, version, at)
    db.refresh(row)
    return row
