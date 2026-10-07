import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class TourRecordStatus(str, enum.Enum):
    completed = "completed"
    skipped = "skipped"
    in_progress = "in_progress"


class UserTour(Base):
    """One row per (account, tour): what the account did with a walkthrough, and at
    which version. See frontend/src/features/tours/ and docs/backend-requests.md §6.

    `at` is the moment the client says the status was set, not when the row was
    written — a queued retry (the client is offline, or a request fails) can reach
    the server after a newer write from the same account already landed, and must
    not roll the record backwards. The service compares `at` before writing, never
    the primary key or the row's own updated-at.
    """
    __tablename__ = "user_tours"
    __table_args__ = (
        UniqueConstraint("user_id", "tour_id", name="uq_user_tour"),
    )

    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tour_id = Column(String(64), nullable=False)
    status  = Column(Enum(TourRecordStatus), nullable=False)
    version = Column(Integer, nullable=False)
    at      = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="tours")
