"""Course commerce records.

Payments are deliberately separated from access: a provider transaction pays
an immutable order snapshot, and that order grants a course enrollment.  The
learning layer reads only the enrollment.
"""
import secrets
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer,
    JSON, String, Text, UniqueConstraint, event, text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


_REFERENCE_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"


def generate_reference_number(now: datetime | None = None) -> str:
    """Return a customer-safe, non-sequential Masar payment reference."""
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%d")
    token = "".join(secrets.choice(_REFERENCE_ALPHABET) for _ in range(8))
    return f"MSR-{stamp}-{token}"


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
        # legacy_free: enrolled while the course was free, kept on the Free/Pro
        # launch (migration 021); an entitlement like purchase/admin_grant.
        CheckConstraint(
            "source IN ('purchase', 'admin_grant', 'free', 'legacy_free')", name="ck_course_enrollments_source",
        ),
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


class CourseFreeLegacy(Base):
    """Every course's `is_free` as it was before migration 021 switched the flag off."""
    __tablename__ = "course_free_legacy"

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    was_free = Column(Boolean, nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class CourseEnrollmentLegacyFree(Base):
    """An enrollment migration 021 grandfathered to `legacy_free`, with what it was before."""
    __tablename__ = "course_enrollment_legacy_free"

    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    previous_source = Column(String(32), nullable=False)
    granted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class BillingPlan(Base):
    """Backend-owned plan catalogue. Amounts are integer piastres."""
    __tablename__ = "billing_plans"
    __table_args__ = (
        CheckConstraint("currency = 'EGP'", name="ck_billing_plans_egp_only"),
        CheckConstraint("monthly_price_minor >= 0", name="ck_billing_plans_monthly_nonnegative"),
        CheckConstraint("yearly_price_minor >= 0", name="ck_billing_plans_yearly_nonnegative"),
    )

    id = Column(Integer, primary_key=True)
    code = Column(String(32), nullable=False, unique=True, index=True)
    name = Column(String(80), nullable=False)
    currency = Column(String(3), nullable=False, default="EGP", server_default="EGP")
    monthly_price_minor = Column(Integer, nullable=False)
    yearly_price_minor = Column(Integer, nullable=False)
    # One-time credits granted at signup. Pro currently changes content
    # access only, so this is deliberately not a monthly allowance.
    signup_credits = Column(Integer, nullable=False, default=0, server_default="0")
    features = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"), index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class UserSubscription(Base):
    """Subscription state derived only from confirmed provider events."""
    __tablename__ = "user_subscriptions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('trialing', 'active', 'past_due', 'cancelled', 'expired')",
            name="ck_user_subscriptions_status",
        ),
        CheckConstraint("billing_period IN ('monthly', 'yearly')", name="ck_user_subscriptions_period"),
        UniqueConstraint("payment_provider", "provider_subscription_id", name="uq_subscription_provider_id"),
        Index("ix_user_subscriptions_user_period", "user_id", "current_period_end"),
        Index(
            "uq_user_subscriptions_one_trial", "user_id", unique=True,
            postgresql_where=text("payment_provider = 'internal'"),
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("billing_plans.id", ondelete="RESTRICT"), nullable=False)
    status = Column(String(20), nullable=False, default="active", server_default="active", index=True)
    billing_period = Column(String(16), nullable=False)
    payment_provider = Column(String(32), nullable=False)
    provider_customer_id = Column(String(100), nullable=True)
    provider_subscription_id = Column(String(100), nullable=True)
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    cancel_at_period_end = Column(Boolean, nullable=False, default=False, server_default=text("false"))
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("BillingPlan")


class SubscriptionOrder(Base):
    """Immutable, server-priced subscription checkout snapshot."""
    __tablename__ = "subscription_orders"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'paid', 'failed', 'cancelled', 'refunded')",
            name="ck_subscription_orders_status",
        ),
        CheckConstraint("billing_period IN ('monthly', 'yearly')", name="ck_subscription_orders_period"),
        CheckConstraint("amount > 0", name="ck_subscription_orders_amount_positive"),
        CheckConstraint("currency = 'EGP'", name="ck_subscription_orders_egp_only"),
        CheckConstraint(
            "refund_status IN ('not_requested', 'requested', 'under_review', 'approved', "
            "'rejected', 'processing', 'refunded', 'failed')",
            name="ck_subscription_orders_refund_status",
        ),
        CheckConstraint(
            "refund_amount IS NULL OR (refund_amount > 0 AND refund_amount <= amount)",
            name="ck_subscription_orders_refund_amount",
        ),
        Index(
            "uq_subscription_orders_one_pending", "user_id", unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
        Index(
            "ix_subscription_orders_provider_transaction_id", "provider_transaction_id", unique=True,
            postgresql_where=text("provider_transaction_id IS NOT NULL"),
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("billing_plans.id", ondelete="RESTRICT"), nullable=False)
    billing_period = Column(String(16), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)
    provider = Column(String(32), nullable=False)
    # Masar's public support reference. Generated before insert, immutable,
    # non-sequential, and deliberately separate from every provider id.
    reference_number = Column(String(32), nullable=False, unique=True, index=True)
    merchant_order_id = Column(String(100), nullable=False, unique=True, index=True)
    provider_order_id = Column(String(100), nullable=True, index=True)
    provider_transaction_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="pending", server_default="pending", index=True)
    refund_requested_at = Column(DateTime(timezone=True), nullable=True)
    refund_processed_at = Column(DateTime(timezone=True), nullable=True)
    refund_amount = Column(Integer, nullable=True)
    refund_reason = Column(Text, nullable=True)
    refund_status = Column(
        String(20), nullable=False, default="not_requested", server_default="not_requested", index=True,
    )
    refund_provider_reference = Column(String(100), nullable=True)
    refund_admin_note = Column(Text, nullable=True)
    subscription_id = Column(Integer, ForeignKey("user_subscriptions.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    plan = relationship("BillingPlan")
    events = relationship("SubscriptionPaymentEvent", back_populates="order")
    refund_events = relationship(
        "SubscriptionRefundEvent", back_populates="order", order_by="SubscriptionRefundEvent.created_at",
    )


class SubscriptionPaymentEvent(Base):
    """One provider event, unique for replay-safe webhook processing."""
    __tablename__ = "subscription_payment_events"
    __table_args__ = (
        UniqueConstraint("provider", "provider_event_id", name="uq_subscription_payment_provider_event"),
        Index("ix_subscription_payment_order_created", "order_id", "created_at"),
        # An order buys exactly one billing period (migration 034).
        Index(
            "uq_subscription_payment_one_grant", "order_id", unique=True,
            postgresql_where=text("grants_period"),
        ),
    )

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("subscription_orders.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(32), nullable=False)
    provider_event_id = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)
    success = Column(Boolean, nullable=False)
    pending = Column(Boolean, nullable=False, default=False, server_default=text("false"))
    response_code = Column(String(100), nullable=True)
    raw_payload = Column(JSON, nullable=False)
    # True only on the event that started or extended the subscription.
    grants_period = Column(Boolean, nullable=False, default=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    order = relationship("SubscriptionOrder", back_populates="events")


class SubscriptionRefundEvent(Base):
    """Append-only audit record for each refund request/state transition."""
    __tablename__ = "subscription_refund_events"
    __table_args__ = (
        CheckConstraint(
            "to_status IN ('requested', 'under_review', 'approved', 'rejected', "
            "'processing', 'refunded', 'failed')",
            name="ck_subscription_refund_events_to_status",
        ),
        UniqueConstraint("idempotency_key", name="uq_subscription_refund_idempotency"),
        Index("ix_subscription_refund_order_created", "order_id", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("subscription_orders.id", ondelete="RESTRICT"), nullable=False)
    from_status = Column(String(20), nullable=False)
    to_status = Column(String(20), nullable=False)
    actor_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    idempotency_key = Column(String(100), nullable=False)
    provider_reference = Column(String(100), nullable=True)
    note = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=False, default=dict, server_default=text("'{}'::json"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    order = relationship("SubscriptionOrder", back_populates="refund_events")
    actor = relationship("User")


@event.listens_for(SubscriptionOrder, "before_insert")
def _subscription_order_reference(_mapper, _connection, target: SubscriptionOrder) -> None:
    # Covers every server-side creation path, including background jobs and
    # tests. The database unique index remains the final concurrency guard.
    if not target.reference_number:
        target.reference_number = generate_reference_number()


class ProAiUsage(Base):
    """One AI action paid from a Pro subscriber's included allowance.

    `reserved` before the provider call, `consumed` once the request succeeded,
    `released` when it failed or never answered (the credits come back, and
    `release_reason` says why). Consumed rows, and reserved rows still within the
    reservation lifetime, count against the rolling window from `reserved_at`, so
    a call that runs across a window boundary is counted exactly once, at the
    moment it was let through. See app/services/billing/pro_ai_allowance.py."""

    __tablename__ = "pro_ai_usage"
    __table_args__ = (
        CheckConstraint("status IN ('reserved', 'consumed', 'released')", name="ck_pro_ai_usage_status"),
        CheckConstraint("credits > 0", name="ck_pro_ai_usage_credits_positive"),
        Index("ix_pro_ai_usage_user_reserved", "user_id", "reserved_at"),
        Index(
            "uq_pro_ai_usage_user_request", "user_id", "request_key", unique=True,
            postgresql_where=text("request_key IS NOT NULL"),
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("user_subscriptions.id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(64), nullable=False)
    credits = Column(Integer, nullable=False)
    status = Column(String(16), nullable=False, default="reserved", server_default="reserved")
    request_key = Column(String(160), nullable=True)
    reserved_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    finalized_at = Column(DateTime(timezone=True), nullable=True)
    released_at = Column(DateTime(timezone=True), nullable=True)
    release_reason = Column(String(120), nullable=True)
