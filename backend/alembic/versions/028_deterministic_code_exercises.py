"""Deterministic code exercises and attempt history.

Revision ID: 028_deterministic_code_exercises
Revises: 027_mentor_quiz_translations
Create Date: 2026-10-05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "028_deterministic_code_exercises"
down_revision: Union[str, None] = "027_mentor_quiz_translations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("exercises", sa.Column("exercise_type", sa.String(24), server_default="legacy", nullable=False))
    op.add_column("exercises", sa.Column("language", sa.String(24), nullable=True))
    op.add_column("exercises", sa.Column("pre_exercise_code", sa.Text(), nullable=True))
    op.add_column("exercises", sa.Column("grading_tests", sa.JSON(), nullable=True))
    op.add_column("exercises", sa.Column("hint", sa.Text(), nullable=True))
    op.add_column("exercises", sa.Column("hint_ar", sa.Text(), nullable=True))
    op.add_column("exercises", sa.Column("success_message", sa.Text(), nullable=True))
    op.add_column("exercises", sa.Column("success_message_ar", sa.Text(), nullable=True))
    # Existing scaffolded exercises are code exercises, but remain safely
    # unsupported until authors add deterministic tests.
    op.execute("UPDATE exercises SET exercise_type = 'code', language = 'python' WHERE starter_code IS NOT NULL")
    op.create_table(
        "code_exercise_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action", sa.String(16), nullable=False),
        sa.Column("submission", sa.Text(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("passed", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("failed_test_id", sa.String(160), nullable=True),
        sa.Column("tests_passed", sa.Integer(), server_default="0", nullable=False),
        sa.Column("tests_total", sa.Integer(), server_default="0", nullable=False),
        sa.Column("execution_time_ms", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_code_exercise_attempts_id", "code_exercise_attempts", ["id"])
    op.create_index(
        "ix_code_exercise_attempt_user_exercise", "code_exercise_attempts", ["user_id", "exercise_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_code_exercise_attempt_user_exercise", table_name="code_exercise_attempts")
    op.drop_index("ix_code_exercise_attempts_id", table_name="code_exercise_attempts")
    op.drop_table("code_exercise_attempts")
    for name in (
        "success_message_ar", "success_message", "hint_ar", "hint", "grading_tests",
        "pre_exercise_code", "language", "exercise_type",
    ):
        op.drop_column("exercises", name)
