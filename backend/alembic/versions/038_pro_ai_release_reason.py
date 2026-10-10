"""Repair the Pro AI usage release-reason column after migration drift.

Some local databases applied an earlier form of revision 036 before
``release_reason`` was present in that migration file.  The application now
uses the column to rate-limit repeatedly invalid provider responses, so those
databases fail mentor requests before a provider call is made.

Fresh databases already receive the column from revision 036.  This forward
repair is therefore conditional and leaves those databases unchanged.

Revision ID: 038_pro_ai_release_reason
Revises: 037_mentor_requests
Create Date: 2026-10-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "038_pro_ai_release_reason"
down_revision: Union[str, None] = "037_mentor_requests"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_names() -> set[str]:
    return {
        column["name"]
        for column in sa.inspect(op.get_bind()).get_columns("pro_ai_usage")
    }


def upgrade() -> None:
    if "release_reason" not in _column_names():
        op.add_column(
            "pro_ai_usage",
            sa.Column("release_reason", sa.String(length=120), nullable=True),
        )


def downgrade() -> None:
    # Revision 036 owns this column on a fresh migration graph.  Dropping it
    # here would make a downgrade to 037 differ depending on database history.
    # The repair is intentionally forward-only.
    pass
