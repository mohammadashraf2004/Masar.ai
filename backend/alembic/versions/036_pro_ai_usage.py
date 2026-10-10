"""Pro plan included AI usage: a ledger of allowance reservations

A Pro subscriber's AI actions draw on 50 credits per rolling 4 hours instead of
the wallet. Each action is one row: reserved before the provider call, consumed
or released (with the reason) after it. Nothing else changes; no existing row is
touched.

Revision ID: 036_pro_ai_usage
Revises: 035_subscription_refunds
Create Date: 2026-10-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "036_pro_ai_usage"
down_revision: Union[str, None] = "035_subscription_refunds"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pro_ai_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subscription_id", sa.Integer(),
                  sa.ForeignKey("user_subscriptions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action_type", sa.String(64), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="reserved"),
        sa.Column("request_key", sa.String(160), nullable=True),
        sa.Column("reserved_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("finalized_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("release_reason", sa.String(120), nullable=True),
        sa.CheckConstraint("status IN ('reserved', 'consumed', 'released')", name="ck_pro_ai_usage_status"),
        sa.CheckConstraint("credits > 0", name="ck_pro_ai_usage_credits_positive"),
    )
    op.create_index("ix_pro_ai_usage_user_reserved", "pro_ai_usage", ["user_id", "reserved_at"])
    op.create_index(
        "uq_pro_ai_usage_user_request", "pro_ai_usage", ["user_id", "request_key"], unique=True,
        postgresql_where=sa.text("request_key IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_pro_ai_usage_user_request", table_name="pro_ai_usage")
    op.drop_index("ix_pro_ai_usage_user_reserved", table_name="pro_ai_usage")
    op.drop_table("pro_ai_usage")
