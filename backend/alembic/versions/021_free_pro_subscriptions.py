"""Free-to-Pro plans, subscriptions, and the idempotent free-credit floor.

Data changes, and how each can be understood or undone (release decision 2026-10-07):

* Course free flags. Every course's previous `is_free` is copied to
  `course_free_legacy` before the flag is switched off, so the old catalogue
  state is never lost; downgrade restores it from there.
* Learners already enrolled in a course while it was free keep that course: their
  active `source='free'` enrollment becomes `source='legacy_free'`, which the
  access layer already treats as an entitlement (anything but 'free'). Each
  conversion is recorded in `course_enrollment_legacy_free` with its previous
  source; downgrade reverts them. Nobody who had not enrolled gains anything.
* Wallets. Eligible free students are raised to AT LEAST 40 credits; a balance
  at or above 40 is never reduced. One `free_plan_40_migration_v1` ledger row per
  raised wallet, so a second run changes nothing.

Revision ID: 021_free_pro_subscriptions
Revises: 020_user_tours
Create Date: 2026-09-27
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "021_free_pro_subscriptions"
down_revision: Union[str, None] = "020_user_tours"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "billing_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(32), nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="EGP"),
        sa.Column("monthly_price_minor", sa.Integer(), nullable=False),
        sa.Column("yearly_price_minor", sa.Integer(), nullable=False),
        sa.Column("signup_credits", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("features", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("currency = 'EGP'", name="ck_billing_plans_egp_only"),
        sa.CheckConstraint("monthly_price_minor >= 0", name="ck_billing_plans_monthly_nonnegative"),
        sa.CheckConstraint("yearly_price_minor >= 0", name="ck_billing_plans_yearly_nonnegative"),
    )
    op.create_index("ix_billing_plans_code", "billing_plans", ["code"], unique=True)
    op.create_index("ix_billing_plans_is_active", "billing_plans", ["is_active"])

    op.create_table(
        "user_subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("billing_plans.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("billing_period", sa.String(16), nullable=False),
        sa.Column("payment_provider", sa.String(32), nullable=False),
        sa.Column("provider_customer_id", sa.String(100), nullable=True),
        sa.Column("provider_subscription_id", sa.String(100), nullable=True),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cancel_at_period_end", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("status IN ('active', 'past_due', 'cancelled', 'expired')", name="ck_user_subscriptions_status"),
        sa.CheckConstraint("billing_period IN ('monthly', 'yearly')", name="ck_user_subscriptions_period"),
        sa.UniqueConstraint("payment_provider", "provider_subscription_id", name="uq_subscription_provider_id"),
    )
    op.create_index("ix_user_subscriptions_user_id", "user_subscriptions", ["user_id"])
    op.create_index("ix_user_subscriptions_status", "user_subscriptions", ["status"])
    op.create_index("ix_user_subscriptions_current_period_end", "user_subscriptions", ["current_period_end"])
    op.create_index("ix_user_subscriptions_user_period", "user_subscriptions", ["user_id", "current_period_end"])

    op.create_table(
        "subscription_orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("billing_plans.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("billing_period", sa.String(16), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("merchant_order_id", sa.String(100), nullable=False),
        sa.Column("provider_order_id", sa.String(100), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status IN ('pending', 'paid', 'failed', 'cancelled', 'refunded')", name="ck_subscription_orders_status"),
        sa.CheckConstraint("billing_period IN ('monthly', 'yearly')", name="ck_subscription_orders_period"),
        sa.CheckConstraint("amount > 0", name="ck_subscription_orders_amount_positive"),
        sa.CheckConstraint("currency = 'EGP'", name="ck_subscription_orders_egp_only"),
    )
    op.create_index("ix_subscription_orders_user_id", "subscription_orders", ["user_id"])
    op.create_index("ix_subscription_orders_merchant_order_id", "subscription_orders", ["merchant_order_id"], unique=True)
    op.create_index("ix_subscription_orders_provider_order_id", "subscription_orders", ["provider_order_id"])
    op.create_index("ix_subscription_orders_status", "subscription_orders", ["status"])
    op.create_index(
        "uq_subscription_orders_one_pending", "subscription_orders", ["user_id"], unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )

    op.create_table(
        "subscription_payment_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("subscription_orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("provider_event_id", sa.String(100), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("pending", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("response_code", sa.String(100), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("provider", "provider_event_id", name="uq_subscription_payment_provider_event"),
    )
    op.create_index("ix_subscription_payment_order_created", "subscription_payment_events", ["order_id", "created_at"])

    # Prices are stored once, in minor units. No Pro credits are fabricated:
    # the existing wallet remains the spend control until usage data supports
    # a recurring allowance.
    op.execute(sa.text("""
        INSERT INTO billing_plans
            (code, name, currency, monthly_price_minor, yearly_price_minor,
             signup_credits, features, is_active)
        VALUES
            ('free', 'Free', 'EGP', 0, 0, 40,
             '["billing.plan.free.f1", "billing.plan.free.f2", "billing.plan.free.f3"]'::json, true),
            ('pro', 'Pro', 'EGP', 29900, 219900, 0,
             '["billing.plan.pro.f1", "billing.plan.pro.f2", "billing.plan.pro.f3", "billing.plan.pro.f4"]'::json, true)
        ON CONFLICT (code) DO UPDATE SET
            name = EXCLUDED.name,
            currency = EXCLUDED.currency,
            monthly_price_minor = EXCLUDED.monthly_price_minor,
            yearly_price_minor = EXCLUDED.yearly_price_minor,
            signup_credits = EXCLUDED.signup_credits,
            features = EXCLUDED.features,
            is_active = EXCLUDED.is_active
    """))

    # The plan model supersedes the old whole-course-free flag. Existing
    # purchases/admin grants remain untouched and still grant full access.
    # Keep what the catalogue looked like, then grandfather the learners who
    # enrolled while a course was free, and only then switch the flags off.
    op.create_table(
        "course_free_legacy",
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("was_free", sa.Boolean(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.execute(sa.text("""
        INSERT INTO course_free_legacy (course_id, was_free)
        SELECT id, COALESCE(is_free, false) FROM courses
        ON CONFLICT (course_id) DO NOTHING
    """))
    op.create_table(
        "course_enrollment_legacy_free",
        sa.Column("enrollment_id", sa.Integer(), sa.ForeignKey("course_enrollments.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("previous_source", sa.String(32), nullable=False),
        sa.Column("granted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.drop_constraint("ck_course_enrollments_source", "course_enrollments", type_="check")
    op.create_check_constraint(
        "ck_course_enrollments_source", "course_enrollments",
        "source IN ('purchase', 'admin_grant', 'free', 'legacy_free')",
    )
    op.execute(sa.text("""
        WITH grandfathered AS (
            UPDATE course_enrollments ce SET source = 'legacy_free'
            FROM course_free_legacy cfl
            WHERE cfl.course_id = ce.course_id AND cfl.was_free
              AND ce.source = 'free' AND ce.status = 'active'
            RETURNING ce.id, ce.user_id, ce.course_id
        )
        INSERT INTO course_enrollment_legacy_free (enrollment_id, user_id, course_id, previous_source)
        SELECT id, user_id, course_id, 'free' FROM grandfathered
        ON CONFLICT (enrollment_id) DO NOTHING
    """))
    op.execute("UPDATE courses SET is_free = false")
    op.alter_column("courses", "is_free", server_default=sa.text("false"))

    # A wallet can be absent on old/imported accounts. Create it first only
    # for students who have never bought credits/course access.
    op.execute(sa.text("""
        INSERT INTO user_wallets
            (user_id, credit_balance, lifetime_purchased, lifetime_spent,
             promo_credits_remaining, promo_expires_at, is_active)
        SELECT u.id, 0, 0, 0, 0, NULL, true
        FROM users u
        WHERE u.role = 'student'
          AND NOT EXISTS (SELECT 1 FROM user_wallets w WHERE w.user_id = u.id)
          AND NOT EXISTS (
              SELECT 1 FROM course_enrollments ce
              WHERE ce.user_id = u.id AND ce.source IN ('purchase', 'admin_grant')
          )
          AND NOT EXISTS (
              SELECT 1 FROM billing_orders bo WHERE bo.user_id = u.id AND bo.status = 'paid'
          )
    """))

    # Raise, never lower: only wallets below 40 are touched, each gets one
    # auditable ledger row for exactly the credits added, and the marker makes
    # a second run a no-op. Their promo window is closed at the same time so a
    # later promo expiry cannot pull a raised wallet back under the floor;
    # wallets already at or above 40 keep their balance and promo terms.
    op.execute(sa.text("""
        WITH targets AS (
            SELECT w.id AS wallet_id, COALESCE(w.credit_balance, 0) AS old_balance
            FROM user_wallets w
            JOIN users u ON u.id = w.user_id
            WHERE u.role = 'student'
              AND COALESCE(w.credit_balance, 0) < 40
              AND NOT EXISTS (
                  SELECT 1 FROM wallet_transactions paid
                  WHERE paid.wallet_id = w.id
                    AND paid.transaction_type = 'topup'
                    AND paid.status = 'confirmed'
              )
              AND NOT EXISTS (
                  SELECT 1 FROM course_enrollments ce
                  WHERE ce.user_id = u.id AND ce.source IN ('purchase', 'admin_grant')
              )
              AND NOT EXISTS (
                  SELECT 1 FROM billing_orders bo WHERE bo.user_id = u.id AND bo.status = 'paid'
              )
              AND NOT EXISTS (
                  SELECT 1 FROM wallet_transactions done
                  WHERE done.wallet_id = w.id AND done.action_type = 'free_plan_40_migration_v1'
              )
        ), ledger AS (
            INSERT INTO wallet_transactions
                (wallet_id, transaction_type, status, credits, payment_method,
                 description, action_type, balance_after)
            SELECT wallet_id,
                   'bonus'::transactiontype,
                   'confirmed'::transactionstatus,
                   40 - old_balance,
                   'admin'::paymentmethod,
                   'Free plan balance raised to 40 credits',
                   'free_plan_40_migration_v1',
                   40
            FROM targets
            RETURNING wallet_id
        )
        UPDATE user_wallets w
        SET credit_balance = 40,
            promo_credits_remaining = 0,
            promo_expires_at = NULL,
            updated_at = now()
        WHERE w.id IN (SELECT wallet_id FROM ledger)
    """))


def downgrade() -> None:
    # Balances and their audit rows are intentionally not reversed: usage may
    # have happened after upgrade, so a downgrade cannot reconstruct truth.
    op.alter_column("courses", "is_free", server_default=sa.text("true"))
    # Undo the grandfathering and restore the catalogue's free flags exactly.
    op.execute(sa.text("""
        UPDATE course_enrollments ce SET source = l.previous_source
        FROM course_enrollment_legacy_free l WHERE l.enrollment_id = ce.id
    """))
    # Only this migration creates legacy_free; any unrecorded row (made by hand
    # after the upgrade) has no older form than 'free'.
    op.execute("UPDATE course_enrollments SET source = 'free' WHERE source = 'legacy_free'")
    op.execute(sa.text("""
        UPDATE courses c SET is_free = l.was_free FROM course_free_legacy l WHERE l.course_id = c.id
    """))
    op.drop_constraint("ck_course_enrollments_source", "course_enrollments", type_="check")
    op.create_check_constraint(
        "ck_course_enrollments_source", "course_enrollments", "source IN ('purchase', 'admin_grant', 'free')",
    )
    op.drop_table("course_enrollment_legacy_free")
    op.drop_table("course_free_legacy")
    op.drop_index("ix_subscription_payment_order_created", table_name="subscription_payment_events")
    op.drop_table("subscription_payment_events")
    op.drop_index("uq_subscription_orders_one_pending", table_name="subscription_orders")
    op.drop_index("ix_subscription_orders_status", table_name="subscription_orders")
    op.drop_index("ix_subscription_orders_provider_order_id", table_name="subscription_orders")
    op.drop_index("ix_subscription_orders_merchant_order_id", table_name="subscription_orders")
    op.drop_index("ix_subscription_orders_user_id", table_name="subscription_orders")
    op.drop_table("subscription_orders")
    op.drop_index("ix_user_subscriptions_user_period", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_current_period_end", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_status", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_user_id", table_name="user_subscriptions")
    op.drop_table("user_subscriptions")
    op.drop_index("ix_billing_plans_is_active", table_name="billing_plans")
    op.drop_index("ix_billing_plans_code", table_name="billing_plans")
    op.drop_table("billing_plans")
