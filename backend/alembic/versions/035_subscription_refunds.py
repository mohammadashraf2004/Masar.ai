"""Masar references and auditable subscription refunds.

Revision ID: 035_subscription_refunds
Revises: 034_payment_provider_binding
Create Date: 2026-10-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "035_subscription_refunds"
down_revision: Union[str, None] = "034_payment_provider_binding"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


REFUND_STATES = (
    "'not_requested', 'requested', 'under_review', 'approved', "
    "'rejected', 'processing', 'refunded', 'failed'"
)


def upgrade() -> None:
    op.drop_constraint("ck_user_subscriptions_status", "user_subscriptions", type_="check")
    op.create_check_constraint(
        "ck_user_subscriptions_status", "user_subscriptions",
        "status IN ('trialing', 'active', 'past_due', 'cancelled', 'expired')",
    )
    op.create_index(
        "uq_user_subscriptions_one_trial", "user_subscriptions", ["user_id"], unique=True,
        postgresql_where=sa.text("payment_provider = 'internal'"),
    )
    op.add_column("subscription_orders", sa.Column("reference_number", sa.String(32), nullable=True))
    op.add_column("subscription_orders", sa.Column("provider_transaction_id", sa.String(100), nullable=True))
    op.add_column("subscription_orders", sa.Column("refund_requested_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("subscription_orders", sa.Column("refund_processed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("subscription_orders", sa.Column("refund_amount", sa.Integer(), nullable=True))
    op.add_column("subscription_orders", sa.Column("refund_reason", sa.Text(), nullable=True))
    op.add_column(
        "subscription_orders",
        sa.Column("refund_status", sa.String(20), nullable=False, server_default="not_requested"),
    )
    op.add_column("subscription_orders", sa.Column("refund_provider_reference", sa.String(100), nullable=True))
    op.add_column("subscription_orders", sa.Column("refund_admin_note", sa.Text(), nullable=True))
    op.add_column("subscription_orders", sa.Column("subscription_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_subscription_orders_subscription_id", "subscription_orders", "user_subscriptions",
        ["subscription_id"], ["id"], ondelete="SET NULL",
    )

    # Legacy rows receive stable, non-sequential references without relying
    # on a database extension. The full digest fragment makes collisions
    # impractical; the unique index below is still authoritative.
    op.execute(sa.text("""
        UPDATE subscription_orders
        SET reference_number = 'MSR-' || to_char(created_at AT TIME ZONE 'UTC', 'YYYYMMDD') || '-' ||
            upper(substr(md5(merchant_order_id || ':' || id::text), 1, 16))
        WHERE reference_number IS NULL
    """))
    op.alter_column("subscription_orders", "reference_number", nullable=False)
    op.create_index(
        "ix_subscription_orders_reference_number", "subscription_orders", ["reference_number"], unique=True,
    )
    op.create_index(
        "ix_subscription_orders_provider_transaction_id", "subscription_orders",
        ["provider_transaction_id"], unique=True,
        postgresql_where=sa.text("provider_transaction_id IS NOT NULL"),
    )
    op.create_index("ix_subscription_orders_refund_status", "subscription_orders", ["refund_status"])
    op.create_check_constraint(
        "ck_subscription_orders_refund_status", "subscription_orders",
        f"refund_status IN ({REFUND_STATES})",
    )
    op.create_check_constraint(
        "ck_subscription_orders_refund_amount", "subscription_orders",
        "refund_amount IS NULL OR (refund_amount > 0 AND refund_amount <= amount)",
    )

    # Backfill the transaction that actually granted each paid order.
    op.execute(sa.text("""
        UPDATE subscription_orders o
        SET provider_transaction_id = e.provider_event_id
        FROM subscription_payment_events e
        WHERE e.order_id = o.id AND e.grants_period = true
          AND o.provider_transaction_id IS NULL
    """))

    op.create_table(
        "subscription_refund_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "order_id", sa.Integer(),
            sa.ForeignKey("subscription_orders.id", ondelete="RESTRICT"), nullable=False,
        ),
        sa.Column("from_status", sa.String(20), nullable=False),
        sa.Column("to_status", sa.String(20), nullable=False),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("idempotency_key", sa.String(100), nullable=False),
        sa.Column("provider_reference", sa.String(100), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "to_status IN ('requested', 'under_review', 'approved', 'rejected', "
            "'processing', 'refunded', 'failed')",
            name="ck_subscription_refund_events_to_status",
        ),
        sa.UniqueConstraint("idempotency_key", name="uq_subscription_refund_idempotency"),
    )
    op.create_index(
        "ix_subscription_refund_order_created", "subscription_refund_events", ["order_id", "created_at"],
    )

    # References are customer-facing audit identifiers and must never be
    # silently replaced after creation, even by a stray bulk update.
    op.execute(sa.text("""
        CREATE FUNCTION prevent_subscription_reference_change() RETURNS trigger AS $$
        BEGIN
            IF NEW.reference_number IS DISTINCT FROM OLD.reference_number THEN
                RAISE EXCEPTION 'subscription order reference_number is immutable';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """))
    op.execute(sa.text("""
        CREATE TRIGGER trg_subscription_reference_immutable
        BEFORE UPDATE OF reference_number ON subscription_orders
        FOR EACH ROW EXECUTE FUNCTION prevent_subscription_reference_change()
    """))


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_subscription_reference_immutable ON subscription_orders")
    op.execute("DROP FUNCTION IF EXISTS prevent_subscription_reference_change()")
    op.drop_index("ix_subscription_refund_order_created", table_name="subscription_refund_events")
    op.drop_table("subscription_refund_events")
    op.drop_constraint("ck_subscription_orders_refund_amount", "subscription_orders", type_="check")
    op.drop_constraint("ck_subscription_orders_refund_status", "subscription_orders", type_="check")
    op.drop_index("ix_subscription_orders_refund_status", table_name="subscription_orders")
    op.drop_index("ix_subscription_orders_provider_transaction_id", table_name="subscription_orders")
    op.drop_index("ix_subscription_orders_reference_number", table_name="subscription_orders")
    op.drop_constraint("fk_subscription_orders_subscription_id", "subscription_orders", type_="foreignkey")
    for column in (
        "subscription_id", "refund_admin_note", "refund_provider_reference", "refund_status",
        "refund_reason", "refund_amount", "refund_processed_at", "refund_requested_at",
        "provider_transaction_id", "reference_number",
    ):
        op.drop_column("subscription_orders", column)
    op.drop_index("uq_user_subscriptions_one_trial", table_name="user_subscriptions")
    op.drop_constraint("ck_user_subscriptions_status", "user_subscriptions", type_="check")
    op.execute("UPDATE user_subscriptions SET status = 'expired' WHERE status = 'trialing'")
    op.create_check_constraint(
        "ck_user_subscriptions_status", "user_subscriptions",
        "status IN ('active', 'past_due', 'cancelled', 'expired')",
    )
