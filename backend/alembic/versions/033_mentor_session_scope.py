"""Mentor v2: scope each conversation to the lesson (or "general") it is about.

`mentor_sessions.context_topic_id` points at `topics`, so it cannot describe a lesson of an
imported course (those hang off `tool_topics`): every v2 message about a real lesson used to
open a new session and send no history. `context_key` is the conversation's scope -
`lesson:<id>` or `general` - and NULL for the legacy `/mentor/chat` sessions, which v2 never
reads.

Revision ID: 033_mentor_session_scope
Revises: 032_project_lab_overview
Create Date: 2026-10-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "033_mentor_session_scope"
down_revision: Union[str, None] = "032_project_lab_overview"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("mentor_sessions", sa.Column("context_key", sa.String(length=64), nullable=True))
    op.create_index(
        "ix_mentor_sessions_user_context_key", "mentor_sessions", ["user_id", "context_key"],
    )


def downgrade() -> None:
    op.drop_index("ix_mentor_sessions_user_context_key", table_name="mentor_sessions")
    op.drop_column("mentor_sessions", "context_key")
