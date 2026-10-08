"""Mentor v2: cached translations of authored quiz questions, so a question follows the UI language.

Revision ID: 027_mentor_quiz_translations
Revises: 026_mentor_evidence
Create Date: 2026-10-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "027_mentor_quiz_translations"
down_revision: Union[str, None] = "026_mentor_evidence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mentor_quiz_translations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("quiz_id", sa.Integer(), sa.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_index", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(2), nullable=False),
        sa.Column("source_hash", sa.String(64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("quiz_id", "question_index", "language", name="uq_mentor_quiz_translation"),
    )
    op.create_index("ix_mentor_quiz_translations_id", "mentor_quiz_translations", ["id"])


def downgrade() -> None:
    op.drop_index("ix_mentor_quiz_translations_id", table_name="mentor_quiz_translations")
    op.drop_table("mentor_quiz_translations")
