"""course assets: Arabic alt text and caption

An image is one picture for both languages; only what is said about it differs. `alt` and
`caption` stay the English ones, so nothing that reads them changes, and the Arabic lesson
reads these two instead (falling back to the English when they are empty). Additive only:
two nullable columns, rollback is a drop.

Revision ID: 029_course_asset_arabic
Revises: 025_exercise_lesson_id
Create Date: 2026-10-05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "029_course_asset_arabic"
down_revision: Union[str, None] = "025_exercise_lesson_id"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("course_assets", sa.Column("alt_ar", sa.Text(), nullable=True))
    op.add_column("course_assets", sa.Column("caption_ar", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("course_assets", "caption_ar")
    op.drop_column("course_assets", "alt_ar")
