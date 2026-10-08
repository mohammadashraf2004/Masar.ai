"""Project Lab: execution leases, persisted artifacts, milestone skills, final submission.

Revision ID: 031_project_lab_capstone
Revises: 030_project_lab
Create Date: 2026-10-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "031_project_lab_capstone"
down_revision: Union[str, None] = "030_project_lab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("lab_milestones", sa.Column("skills", sa.JSON(), nullable=False, server_default="[]"))
    op.add_column("lab_attempts", sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        "lab_artifacts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("media_type", sa.String(64), nullable=False),
        sa.Column("encoding", sa.String(16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("attempt_id", "path", name="uq_lab_artifacts_attempt_path"),
    )
    op.create_index("ix_lab_artifacts_id", "lab_artifacts", ["id"])
    op.create_index("ix_lab_artifacts_attempt_id", "lab_artifacts", ["attempt_id"])

    op.create_table(
        "lab_execution_leases",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token", sa.String(64), nullable=False),
        sa.Column("action", sa.String(16), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("lab_execution_leases")
    op.drop_index("ix_lab_artifacts_attempt_id", table_name="lab_artifacts")
    op.drop_index("ix_lab_artifacts_id", table_name="lab_artifacts")
    op.drop_table("lab_artifacts")
    op.drop_column("lab_attempts", "submitted_at")
    op.drop_column("lab_milestones", "skills")
