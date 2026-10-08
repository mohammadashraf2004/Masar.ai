"""Career track workflow: explicit order, requiredness and section on course_roles

Adds three columns to the existing `course_roles` association (course <->
career goal): `position` (this course's ordinal slot in that goal's workflow),
`required` (whether it gates the goal's required-completion percentage) and
`section` (AI Engineer's apex path groups into foundations /
language-generative-ai / application-production / advanced-ai-systems /
specializations; every other goal leaves it NULL).

Additive only: no table is created, nothing existing is dropped or renamed,
and the two new non-nullable columns get safe defaults (`position=0`,
`required=true`) so every existing row stays valid without a backfill script.
The data itself (the actual per-goal ordering) is written by
`seeds/sync_curriculum.py`, not by this migration.

Revision ID: 023_career_track_course_workflow
Revises: 022_vocabulary_terms
Create Date: 2026-09-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "023_career_track_course_workflow"
down_revision: Union[str, None] = "022_vocabulary_terms"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "course_roles",
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "course_roles",
        sa.Column("required", sa.Boolean(), nullable=False, server_default="true"),
    )
    op.add_column(
        "course_roles",
        sa.Column("section", sa.String(), nullable=True),
    )
    op.create_check_constraint(
        "ck_course_roles_section",
        "course_roles",
        "section IS NULL OR section IN "
        "('foundations', 'language-generative-ai', 'application-production', "
        "'advanced-ai-systems', 'specializations')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_course_roles_section", "course_roles", type_="check")
    op.drop_column("course_roles", "section")
    op.drop_column("course_roles", "required")
    op.drop_column("course_roles", "position")
