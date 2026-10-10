"""Mentor request claims: one row per paid mentor request id

A retried mentor request (a timeout, a dropped connection, a double click) carries
the same client id as the first. This table's unique (user, action, request id)
is what lets the server tell, without a race, that the request is already running
or already answered - so it is charged and sent to the provider once. No existing
table can hold that claim for wallet learners. Nothing else changes; no existing
row is touched.

Revision ID: 037_mentor_requests
Revises: 036_pro_ai_usage
Create Date: 2026-10-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "037_mentor_requests"
down_revision: Union[str, None] = "036_pro_ai_usage"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mentor_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action", sa.String(40), nullable=False),
        sa.Column("request_id", sa.String(64), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="processing"),
        sa.Column("charged_credits", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("charge_source", sa.String(16), nullable=True),
        sa.Column("response", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "action", "request_id", name="uq_mentor_requests_user_action_request"),
        sa.CheckConstraint("status IN ('processing', 'done', 'failed')", name="ck_mentor_requests_status"),
    )
    op.create_index("ix_mentor_requests_updated_at", "mentor_requests", ["updated_at"])


def downgrade() -> None:
    op.drop_index("ix_mentor_requests_updated_at", table_name="mentor_requests")
    op.drop_table("mentor_requests")
