"""Course commerce records.

Payments are deliberately separated from access: a provider transaction pays
an immutable order snapshot, and that order grants a course enrollment.  The
learning layer reads only the enrollment.
"""
from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer,
    JSON, String, UniqueConstraint, text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class CourseOffer(Base):
    __tablename__ = "course_offers"
    __table_args__ = (
        CheckConstraint("price_amount > 0", name="ck_course_offers_price_positive"),
        CheckConstraint(
            "original_price_amount IS NULL OR original_price_amount >= price_amount",
            name="ck_course_offers_original_price",
        ),
        CheckConstraint("currency = 'EGP'", name="ck_course_offers_egp_only"),
        Index(
            "uq_course_offers_one_active", "course_id", unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    price_amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False, default="EGP", server_default="EGP")
    original_price_amount = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"), index=True)
    starts_at = Column(DateTime(timezone=True), nullable=True)
    ends_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    course = relationship("Course")


class BillingOrder(Base):
    __tablename__ = "billing_orders"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'paid', 'failed', 'cancelled', 'refunded')",
            name="ck_billing_orders_status",
        ),
        CheckConstraint("purchasable_type = 'course'", name="ck_billing_orders_course_v1"),
        CheckConstraint("amount >= 0", name="ck_billing_orders_amount_nonnegative"),
        CheckConstraint("currency = 'EGP'", name="ck_billing_orders_egp_only"),
        Index("ix_billing_orders_user_created", "user_id", "created_at"),
        Index("ix_billing_orders_course_status", "course_id", "status"),
        Index(
            "uq_billing_orders_one_pending_course",
            "user_id", "course_id", unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    purchasable_type = Column(String(32), nullable=False, default="course", server_default="course")
    purchasable_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False, index=True)
    offer_id = Column(Integer, ForeignKey("course_offers.id", ondelete="SET NULL"), nullable=True)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False, default="EGP", server_default="EGP")
    provider = Column(String(32), nullable=False, default="paymob", server_default="paymob")
    merchant_order_id = Column(String(100), nullable=False, unique=True, index=True)
    provider_order_id = Column(String(100), nullable=True, index=True)
    status = Column(String(20), nullable=False, default="pending", server_default="pending", index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    course = relationship("Course")
    offer = relationship("CourseOffer")
    transactions = relationship("PaymentTransaction", back_populates="order")


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    __table_args__ = (
        UniqueConstraint("provider", "provider_transaction_id", name="uq_payment_transactions_provider_id"),
        CheckConstraint("amount >= 0", name="ck_payment_transactions_amount_nonnegative"),
        Index("ix_payment_transactions_order_created", "order_id", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("billing_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(32), nullable=False)
    provider_transaction_id = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)
    success = Column(Boolean, nullable=False)
    pending = Column(Boolean, nullable=False, default=False, server_default=text("false"))
    response_code = Column(String(100), nullable=True)
    raw_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    order = relationship("BillingOrder", back_populates="transactions")


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_course_enrollments_user_course"),
        CheckConstraint("source IN ('purchase', 'admin_grant', 'free')", name="ck_course_enrollments_source"),
        CheckConstraint("status IN ('active', 'revoked', 'expired')", name="ck_course_enrollments_status"),
        CheckConstraint(
            "learning_status IN ('enrolled', 'in_progress', 'completed', 'paused')",
            name="ck_course_enrollments_learning_status",
        ),
        Index("ix_course_enrollments_user_status", "user_id", "status"),
        Index("ix_course_enrollments_course_status", "course_id", "status"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    source = Column(String(32), nullable=False)
    order_id = Column(Integer, ForeignKey("billing_orders.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(String(20), nullable=False, default="active", server_default="active", index=True)
    enrolled_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    # Where the learner is in the course. `status` above is about *access* (active /
    # revoked / expired); this is about *learning*. The lifecycle is a cache of the
    # learner's real progress, which is derived from `user_progress` and never stored:
    # the progress endpoints move it forward and the API recomputes the live percentage
    # on every read. Only `paused` is the learner's own choice.
    learning_status = Column(String(20), nullable=False, default="enrolled", server_default="enrolled")
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User")
    course = relationship("Course")
    order = relationship("BillingOrder")
