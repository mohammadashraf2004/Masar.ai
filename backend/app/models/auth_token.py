"""
backend/app/models/auth_token.py

Single-purpose, single-use tokens for email verification and password
reset. Only the SHA-256 hash of the token is stored — same principle as
password hashing: if the DB leaks, the tokens in it are useless. The
random value itself only ever exists in the email we send and briefly
in memory while validating.
"""
import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class EmailTokenPurpose(str, enum.Enum):
    verify_email    = "verify_email"
    reset_password  = "reset_password"


class EmailToken(Base):
    __tablename__ = "email_tokens"
    # Supports the "retire this user's outstanding tokens of this purpose"
    # sweep that runs every time a new verify/reset link is issued.
    __table_args__ = (Index("ix_email_tokens_user_purpose", "user_id", "purpose"),)

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    purpose     = Column(Enum(EmailTokenPurpose), nullable=False)
    token_hash  = Column(String, unique=True, index=True, nullable=False)
    expires_at  = Column(DateTime(timezone=True), nullable=False)
    used_at     = Column(DateTime(timezone=True), nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="email_tokens")
