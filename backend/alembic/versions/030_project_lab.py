"""Project Lab: project content definitions and learner workspaces.

Revision ID: 030_project_lab
Revises: 028_deterministic_code_exercises
Create Date: 2026-10-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "030_project_lab"
down_revision: Union[str, None] = "028_deterministic_code_exercises"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _timestamps(*names: str) -> list[sa.Column]:
    return [
        sa.Column(name, sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
        for name in names
    ]


def upgrade() -> None:
    op.create_table(
        "lab_projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("track_id", sa.Integer(), sa.ForeignKey("career_tracks.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("title_ar", sa.String(200), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("summary_ar", sa.Text(), nullable=True),
        sa.Column("difficulty", sa.String(24), nullable=False, server_default="beginner"),
        sa.Column("estimated_hours", sa.Integer(), nullable=True),
        sa.Column("template_key", sa.String(80), nullable=False),
        sa.Column("template_version", sa.String(40), nullable=False),
        sa.Column("read_only_paths", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_timestamps("created_at", "updated_at"),
    )
    op.create_index("ix_lab_projects_id", "lab_projects", ["id"])
    op.create_index("ix_lab_projects_track_id", "lab_projects", ["track_id"])

    op.create_table(
        "lab_milestones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("lab_projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("title_ar", sa.String(200), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("summary_ar", sa.Text(), nullable=True),
        sa.UniqueConstraint("project_id", "slug", name="uq_lab_milestones_project_slug"),
    )
    op.create_index("ix_lab_milestones_id", "lab_milestones", ["id"])
    op.create_index("ix_lab_milestones_project_id", "lab_milestones", ["project_id"])

    op.create_table(
        "lab_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("lab_projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("milestone_id", sa.Integer(), sa.ForeignKey("lab_milestones.id", ondelete="CASCADE"), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("title_ar", sa.String(200), nullable=True),
        sa.Column("instructions", sa.Text(), nullable=False),
        sa.Column("instructions_ar", sa.Text(), nullable=True),
        sa.Column("hints", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("primary_file", sa.String(255), nullable=True),
        sa.Column("validator_key", sa.String(120), nullable=False),
        sa.Column("validator_config", sa.JSON(), nullable=False, server_default="{}"),
        sa.UniqueConstraint("project_id", "slug", name="uq_lab_tasks_project_slug"),
    )
    op.create_index("ix_lab_tasks_id", "lab_tasks", ["id"])
    op.create_index("ix_lab_tasks_project_id", "lab_tasks", ["project_id"])
    op.create_index("ix_lab_tasks_milestone_id", "lab_tasks", ["milestone_id"])

    op.create_table(
        "lab_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("lab_projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("template_version", sa.String(40), nullable=False),
        *_timestamps("started_at", "updated_at"),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "project_id", name="uq_lab_attempts_user_project"),
    )
    op.create_index("ix_lab_attempts_id", "lab_attempts", ["id"])
    op.create_index("ix_lab_attempts_user_id", "lab_attempts", ["user_id"])
    op.create_index("ix_lab_attempts_project_id", "lab_attempts", ["project_id"])

    op.create_table(
        "lab_workspace_files",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        *_timestamps("updated_at"),
        sa.UniqueConstraint("attempt_id", "path", name="uq_lab_workspace_files_attempt_path"),
    )
    op.create_index("ix_lab_workspace_files_id", "lab_workspace_files", ["id"])
    op.create_index("ix_lab_workspace_files_attempt_id", "lab_workspace_files", ["attempt_id"])

    op.create_table(
        "lab_task_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("lab_tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="not_started"),
        sa.Column("check_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_outcome", sa.String(8), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("attempt_id", "task_id", name="uq_lab_task_progress_attempt_task"),
    )
    op.create_index("ix_lab_task_progress_id", "lab_task_progress", ["id"])
    op.create_index("ix_lab_task_progress_attempt_id", "lab_task_progress", ["attempt_id"])
    op.create_index("ix_lab_task_progress_task_id", "lab_task_progress", ["task_id"])

    op.create_table(
        "lab_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("execution_ms", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps("created_at"),
    )
    op.create_index("ix_lab_runs_id", "lab_runs", ["id"])
    op.create_index("ix_lab_runs_attempt_created", "lab_runs", ["attempt_id", "created_at"])

    op.create_table(
        "lab_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("lab_tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("outcome", sa.String(8), nullable=False),
        sa.Column("checks", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("error_kind", sa.String(24), nullable=True),
        sa.Column("execution_ms", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps("created_at"),
    )
    op.create_index("ix_lab_submissions_id", "lab_submissions", ["id"])
    op.create_index("ix_lab_submissions_attempt_task", "lab_submissions", ["attempt_id", "task_id"])


def downgrade() -> None:
    for table, indexes in (
        ("lab_submissions", ["ix_lab_submissions_attempt_task", "ix_lab_submissions_id"]),
        ("lab_runs", ["ix_lab_runs_attempt_created", "ix_lab_runs_id"]),
        ("lab_task_progress", ["ix_lab_task_progress_task_id", "ix_lab_task_progress_attempt_id", "ix_lab_task_progress_id"]),
        ("lab_workspace_files", ["ix_lab_workspace_files_attempt_id", "ix_lab_workspace_files_id"]),
        ("lab_attempts", ["ix_lab_attempts_project_id", "ix_lab_attempts_user_id", "ix_lab_attempts_id"]),
        ("lab_tasks", ["ix_lab_tasks_milestone_id", "ix_lab_tasks_project_id", "ix_lab_tasks_id"]),
        ("lab_milestones", ["ix_lab_milestones_project_id", "ix_lab_milestones_id"]),
        ("lab_projects", ["ix_lab_projects_track_id", "ix_lab_projects_id"]),
    ):
        for index in indexes:
            op.drop_index(index, table_name=table)
        op.drop_table(table)
