"""Bind Paymob callbacks to the provider order they paid, at most once.

Paymob's callback HMAC does not cover `order.merchant_order_id`, so that field
alone cannot say which of our records a signed transaction settles. Wallet
top-ups and exam payments therefore record the Paymob order id created at
checkout (`provider_order_id`, which IS signed) and the transaction id that
settled them (`provider_transaction_id`, unique: one Paymob transaction can
settle one record).

A subscription order may receive several callbacks (a decline then a retry,
a refund, a void, a capture). `subscription_payment_events.grants_period`
marks the one event that started or extended the subscription, and a partial
unique index makes a second granting event for the same order impossible.

Additive only. Pending rows created before this revision have no
provider_order_id; the webhook leaves them for manual review instead of
settling them.

Revision ID: 034_payment_provider_binding
Revises: 033_mentor_session_scope
Create Date: 2026-10-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "034_payment_provider_binding"
down_revision: Union[str, None] = "033_mentor_session_scope"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for table in ("wallet_transactions", "exam_payments"):
        op.add_column(table, sa.Column("provider_order_id", sa.String(100), nullable=True))
        op.add_column(table, sa.Column("provider_transaction_id", sa.String(100), nullable=True))
        op.create_index(
            f"uq_{table}_provider_txn", table, ["provider_transaction_id"], unique=True,
            postgresql_where=sa.text("provider_transaction_id IS NOT NULL"),
        )

    op.add_column(
        "subscription_payment_events",
        sa.Column("grants_period", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    # Existing paid orders: the earliest clean success is the one that granted.
    op.execute(sa.text("""
        UPDATE subscription_payment_events SET grants_period = true
        WHERE id IN (
            SELECT min(e.id) FROM subscription_payment_events e
            JOIN subscription_orders o ON o.id = e.order_id
            WHERE o.status = 'paid' AND e.success AND NOT e.pending AND e.response_code IS NULL
            GROUP BY e.order_id
        )
    """))
    op.create_index(
        "uq_subscription_payment_one_grant", "subscription_payment_events", ["order_id"], unique=True,
        postgresql_where=sa.text("grants_period"),
    )


def downgrade() -> None:
    op.drop_index("uq_subscription_payment_one_grant", table_name="subscription_payment_events")
    op.drop_column("subscription_payment_events", "grants_period")
    for table in ("exam_payments", "wallet_transactions"):
        op.drop_index(f"uq_{table}_provider_txn", table_name=table)
        op.drop_column(table, "provider_transaction_id")
        op.drop_column(table, "provider_order_id")
