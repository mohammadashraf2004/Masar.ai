"""Let an exercise declare the single lesson it is graded against.

Revision ID: 025_exercise_lesson_id
Revises: 024_optional_course_modules
Create Date: 2026-09-28
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "025_exercise_lesson_id"
down_revision: Union[str, None] = "024_optional_course_modules"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("exercises", sa.Column("lesson_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_exercises_lesson_id", "exercises", "lessons", ["lesson_id"], ["id"],
    )
    op.create_index("ix_exercises_lesson_id", "exercises", ["lesson_id"])


def downgrade() -> None:
    op.drop_index("ix_exercises_lesson_id", table_name="exercises")
    op.drop_constraint("fk_exercises_lesson_id", "exercises", type_="foreignkey")
    op.drop_column("exercises", "lesson_id")
