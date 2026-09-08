"""
app/models/vocabulary.py

English-terminology progress per user.

The point of the Arabic-first policy is that a student understands the
concept in Arabic *and* can name it in English — the naming half is what
shows up in documentation, interviews and job descriptions. This table is
how that half is measured.

`term_id` references the terminology dictionary
(`app/content/ai_terms.json`), not a database table. The dictionary is a
content asset authored in the frontend and exported; making it a table would
mean a migration every time an author adds a term. Unknown ids are rejected
at the controller boundary instead, against the loaded dictionary.
"""
import enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class TermStatus(str, enum.Enum):
    #: Seen introduced in a lesson — read, not yet proven.
    encountered = "encountered"
    #: Answered correctly about it, or explicitly marked from the glossary.
    learned = "learned"


class UserTermProgress(Base):
    __tablename__ = "user_term_progress"
    __table_args__ = (
        # One row per user per term; the controller upgrades the row's status
        # rather than inserting a second one.
        UniqueConstraint("user_id", "term_id", name="uq_user_term_progress_user_term"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    term_id = Column(String(64), nullable=False, index=True)

    status = Column(Enum(TermStatus), nullable=False, default=TermStatus.encountered)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    learned_at = Column(DateTime(timezone=True), nullable=True)

    # Deliberately one-directional: nothing loads a user in order to walk
    # their vocabulary rows, and the reverse collection would be a few
    # hundred rows per user that no other query wants.
    user = relationship("User")
