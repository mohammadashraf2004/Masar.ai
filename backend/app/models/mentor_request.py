from sqlalchemy import JSON, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from app.db.session import Base


class MentorRequest(Base):
    """One paid mentor request, named by the id the client gave it (migration 037).

    The unique (user, action, request id) row is the claim: the first request inserts it as
    `processing` and is the only one that may charge and call the provider; a duplicate that
    arrives while it runs is told to retry, and one that arrives after it finished gets the
    stored `response` back, free. `charged_credits`/`charge_source` say what the owner took and
    has not given back, so a request whose worker died can be refunded by the next claim.
    See app/services/mentor/idempotency.py."""

    __tablename__ = "mentor_requests"
    __table_args__ = (
        UniqueConstraint("user_id", "action", "request_id", name="uq_mentor_requests_user_action_request"),
        CheckConstraint("status IN ('processing', 'done', 'failed')", name="ck_mentor_requests_status"),
        Index("ix_mentor_requests_updated_at", "updated_at"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(40), nullable=False)
    request_id = Column(String(64), nullable=False)
    status = Column(String(16), nullable=False, default="processing", server_default="processing")
    charged_credits = Column(Integer, nullable=False, default=0, server_default="0")
    charge_source = Column(String(16), nullable=True)
    response = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
