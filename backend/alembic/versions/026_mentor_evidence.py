"""Mentor v2: the evidence behind a learner's skill state and the mentor's memory of mistakes.

Revision ID: 026_mentor_evidence
Revises: 023_career_track_course_workflow
Create Date: 2026-10-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "026_mentor_evidence"
down_revision: Union[str, None] = "023_career_track_course_workflow"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mentor_evidence",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(20), nullable=False, server_default="quiz"),
        sa.Column("skill", sa.String(120), nullable=False),
        sa.Column("correct", sa.Boolean(), nullable=False),
        sa.Column("quiz_id", sa.Integer(), sa.ForeignKey("quizzes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("question_index", sa.Integer(), nullable=True),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True),
        sa.Column("selected", sa.Integer(), nullable=True),
        sa.Column("attempt_no", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_mentor_evidence_id", "mentor_evidence", ["id"])
    op.create_index("ix_mentor_evidence_user_skill_created", "mentor_evidence", ["user_id", "skill", "created_at"])
    op.create_index("ix_mentor_evidence_user_lesson", "mentor_evidence", ["user_id", "lesson_id"])


def downgrade() -> None:
    op.drop_index("ix_mentor_evidence_user_lesson", table_name="mentor_evidence")
    op.drop_index("ix_mentor_evidence_user_skill_created", table_name="mentor_evidence")
    op.drop_index("ix_mentor_evidence_id", table_name="mentor_evidence")
    op.drop_table("mentor_evidence")
