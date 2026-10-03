"""course assets: the figures a lesson places inline

A lesson body places a figure with `{{figure:<key>}}` on a line of its own. This
adds the table that says what each key is - alt text, caption, type, size, hash -
and where its bytes are stored. Additive only: a new table, nothing altered, so
courses without figures (COURSE-001 to 007) are untouched and rollback is a drop.

Revision ID: 019_course_assets
Revises: 018_independent_enrollment
Create Date: 2026-09-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "019_course_assets"
down_revision: Union[str, None] = "018_independent_enrollment"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "course_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tool_course_id", sa.Integer(), sa.ForeignKey("tool_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key", sa.String(120), nullable=False),
        sa.Column("asset_type", sa.String(20), nullable=False, server_default="image"),
        sa.Column("storage_key", sa.String(500), nullable=False),
        sa.Column("mime_type", sa.String(60), nullable=False),
        sa.Column("byte_size", sa.BigInteger(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("alt", sa.Text(), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("figure_number", sa.String(40), nullable=True),
        sa.Column("source_reference", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("tool_course_id", "key", name="uq_course_assets_course_key"),
    )
    op.create_index("ix_course_assets_id", "course_assets", ["id"])
    op.create_index("ix_course_assets_tool_course_id", "course_assets", ["tool_course_id"])


def downgrade() -> None:
    op.drop_index("ix_course_assets_tool_course_id", table_name="course_assets")
    op.drop_index("ix_course_assets_id", table_name="course_assets")
    op.drop_table("course_assets")
