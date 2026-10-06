"""Persist whether a course module counts toward course completion.

Revision ID: 024_optional_course_modules
Revises: 019_course_assets
Create Date: 2026-09-28
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "024_optional_course_modules"
down_revision: Union[str, None] = "019_course_assets"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tool_topics",
        sa.Column("is_optional", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "tool_topics",
        sa.Column("completion_required", sa.Boolean(), nullable=False, server_default="true"),
    )


def downgrade() -> None:
    op.drop_column("tool_topics", "completion_required")
    op.drop_column("tool_topics", "is_optional")
