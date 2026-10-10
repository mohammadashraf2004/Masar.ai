"""Example answers for written exercises.

Written (AI-evaluated) exercises had no reference answer at all, so learners
had nothing to compare their answer with and the evaluator graded without a
reference. Two nullable columns hold one good answer per language; the API
shows it only after the learner's first evaluated answer.

Numbered 040 because a concurrent, not yet integrated stream owns 039
(039_additional_credit_packs). If that revision lands first, point
down_revision at it; both migrations only add independent nullable columns.

Revision ID: 040_exercise_example_answers
Revises: 038_pro_ai_release_reason
Create Date: 2026-10-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "040_exercise_example_answers"
down_revision: Union[str, None] = "038_pro_ai_release_reason"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("exercises", sa.Column("example_answer", sa.Text(), nullable=True))
    op.add_column("exercises", sa.Column("example_answer_ar", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("exercises", "example_answer_ar")
    op.drop_column("exercises", "example_answer")
