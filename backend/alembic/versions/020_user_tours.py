"""per-account walkthrough (tour) progress

One row per (account, tour), replacing the client-only `localStorage["masar.tours"]`
(frontend/src/features/tours/records.ts) as the record of what an account did with
each onboarding/feature walkthrough. Additive only: a new table, nothing altered.

See docs/backend-requests.md §6.

Chain order is not numeric order: 024, 025 and 029 were committed first,
directly on top of 019, so a database can already be at 029 without 020-023 or
026-028. Those seven therefore run after 029 (029 -> 020..023 -> 026..028 ->
030). Never re-parent 024/025/029; tests/test_migration_graph.py guards this.

Revision ID: 020_user_tours
Revises: 029_course_asset_arabic
Create Date: 2026-09-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "020_user_tours"
down_revision: Union[str, None] = "029_course_asset_arabic"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_tours",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tour_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.Enum("completed", "skipped", "in_progress", name="tourrecordstatus"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "tour_id", name="uq_user_tour"),
    )
    op.create_index("ix_user_tours_user_id", "user_tours", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_user_tours_user_id", table_name="user_tours")
    op.drop_table("user_tours")
    op.execute("DROP TYPE IF EXISTS tourrecordstatus")
