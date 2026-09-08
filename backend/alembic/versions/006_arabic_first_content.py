"""arabic-first content and terminology progress

Two things:

1. An optional Arabic twin for every learner-facing text column, plus the
   technical-terminology metadata a course exposes. Every column is nullable
   and nothing reads them as required — a course seeded before the
   Arabic-first policy renders exactly as it did, and the API falls back to
   the English field when no Arabic version exists.

   Deliberately absent: an `_ar` twin for `starter_code`, `solution_code`
   and `tech_stack`. Code, identifiers and framework names are identical in
   every language, and giving them a translatable column would invite
   exactly the mistake the policy exists to prevent.

2. `user_term_progress` — which English terms a student has met and which
   they have proven. `term_id` is a dictionary key from
   app/content/ai_terms.json, not a foreign key: the dictionary is an
   authored content asset, and adding a term must not require a migration.

Revision ID: 006_arabic_first_content
Revises: 005_launch_promo_credits
Create Date: 2026-09-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '006_arabic_first_content'
down_revision: Union[str, None] = '005_launch_promo_credits'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# (table, column, type) for every added bilingual/metadata column.
_TEXT_COLUMNS = [
    ('career_tracks', 'title_ar', sa.String()),
    ('career_tracks', 'description_ar', sa.Text()),
    ('track_levels', 'title_ar', sa.String()),
    ('track_levels', 'description_ar', sa.Text()),
    ('topics', 'title_ar', sa.String()),
    ('topics', 'description_ar', sa.Text()),
    ('lessons', 'title_ar', sa.String()),
    ('lessons', 'content_ar', sa.Text()),
    ('exercises', 'title_ar', sa.String()),
    ('exercises', 'description_ar', sa.Text()),
    ('projects', 'title_ar', sa.String()),
    ('projects', 'description_ar', sa.Text()),
    ('quizzes', 'title_ar', sa.String()),
    ('tool_courses', 'title_ar', sa.String()),
    ('tool_courses', 'description_ar', sa.Text()),
    ('tool_topics', 'title_ar', sa.String()),
    ('tool_topics', 'description_ar', sa.Text()),
]

_JSON_COLUMNS = [
    ('quizzes', 'questions_ar'),
    ('topics', 'technical_terms'),
    ('tool_courses', 'technical_terms'),
    ('tool_courses', 'industry_skills'),
    ('tool_topics', 'technical_terms'),
]


def upgrade() -> None:
    for table, column, type_ in _TEXT_COLUMNS:
        op.add_column(table, sa.Column(column, type_, nullable=True))

    for table, column in _JSON_COLUMNS:
        op.add_column(table, sa.Column(column, sa.JSON(), nullable=True))

    # The `termstatus` type is created by CREATE TABLE below, and dropped
    # explicitly in downgrade() — same pattern as 001_initial_schema, because
    # DROP TABLE leaves the Postgres ENUM type behind.
    op.create_table(
        'user_term_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('term_id', sa.String(length=64), nullable=False),
        sa.Column('status',
                  sa.Enum('encountered', 'learned', name='termstatus'),
                  nullable=False, server_default='encountered'),
        sa.Column('first_seen_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('learned_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                name='fk_user_term_progress_user_id_users'),
        sa.PrimaryKeyConstraint('id'),
        # One row per user per term — the API upgrades encountered → learned
        # in place rather than accumulating a row per lesson view.
        sa.UniqueConstraint('user_id', 'term_id',
                            name='uq_user_term_progress_user_term'),
    )
    op.create_index(op.f('ix_user_term_progress_id'), 'user_term_progress', ['id'])
    op.create_index(op.f('ix_user_term_progress_user_id'), 'user_term_progress', ['user_id'])
    op.create_index(op.f('ix_user_term_progress_term_id'), 'user_term_progress', ['term_id'])


def downgrade() -> None:
    op.drop_index(op.f('ix_user_term_progress_term_id'), table_name='user_term_progress')
    op.drop_index(op.f('ix_user_term_progress_user_id'), table_name='user_term_progress')
    op.drop_index(op.f('ix_user_term_progress_id'), table_name='user_term_progress')
    op.drop_table('user_term_progress')
    op.execute('DROP TYPE IF EXISTS termstatus')

    for table, column in reversed(_JSON_COLUMNS):
        op.drop_column(table, column)

    for table, column, _ in reversed(_TEXT_COLUMNS):
        op.drop_column(table, column)
