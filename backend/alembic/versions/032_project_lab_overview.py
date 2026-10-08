"""Project Lab: project overview content and the completion snapshot.

Revision ID: 032_project_lab_overview
Revises: 031_project_lab_capstone
Create Date: 2026-10-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "032_project_lab_overview"
down_revision: Union[str, None] = "031_project_lab_capstone"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("lab_projects", sa.Column("overview", sa.JSON(), nullable=False, server_default="{}"))
    op.add_column("lab_attempts", sa.Column("completion", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("lab_attempts", "completion")
    op.drop_column("lab_projects", "overview")
