from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class UserUpdateAcknowledgement(Base):
    """An account has seen one announcement (see app.core.releases).

    One row per (account, announcement), enforced by the unique constraint, so
    acknowledging twice - a double click, two tabs, a retried request - is a
    no-op rather than a duplicate. The identifier is a string the server
    validates against its own list, so a future announcement needs no schema
    change.
    """
    __tablename__ = "user_update_acknowledgements"
    __table_args__ = (
        UniqueConstraint("user_id", "release_id", name="uq_user_update_ack"),
    )

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    release_id      = Column(String(64), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="update_acknowledgements")
