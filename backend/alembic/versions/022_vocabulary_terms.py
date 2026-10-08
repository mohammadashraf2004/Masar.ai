"""AI Vocabulary: a normalized global term dictionary

Adds vocabulary_terms (one canonical row per concept), vocabulary_term_relations
("related terms") and vocabulary_term_associations (which course/module/lesson
teaches a term). Additive only: the old ai_terms.json-backed
`user_term_progress` table is untouched except for a new nullable
`vocabulary_term_id` FK, backfilled after the dictionary is seeded so existing
progress rows survive (their `term_id` string column is never dropped).

Revision ID: 022_vocabulary_terms
Revises: 021_free_pro_subscriptions
Create Date: 2026-09-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "022_vocabulary_terms"
down_revision: Union[str, None] = "021_free_pro_subscriptions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vocabulary_terms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False),
        sa.Column("term_en", sa.String(160), nullable=False),
        sa.Column("term_ar", sa.String(160), nullable=False),
        sa.Column("acronym", sa.String(40), nullable=True),
        sa.Column("aliases", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("category", sa.String(60), nullable=True),
        sa.Column("difficulty", sa.String(20), nullable=False, server_default="intermediate"),
        sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("definition_en", sa.Text(), nullable=False),
        sa.Column("definition_ar", sa.Text(), nullable=False),
        sa.Column("explanation_simple_ar", sa.Text(), nullable=True),
        sa.Column("why_it_matters_ar", sa.Text(), nullable=True),
        sa.Column("example_ar", sa.Text(), nullable=True),
        sa.Column("source_references", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("first_course_key", sa.String(20), nullable=True),
        sa.Column("first_lesson_key", sa.String(20), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_vocabulary_terms_id", "vocabulary_terms", ["id"])
    op.create_index("ix_vocabulary_terms_slug", "vocabulary_terms", ["slug"], unique=True)
    op.create_index("ix_vocabulary_terms_category", "vocabulary_terms", ["category"])
    op.create_index("ix_vocabulary_terms_difficulty", "vocabulary_terms", ["difficulty"])
    op.create_index("ix_vocabulary_terms_first_course_key", "vocabulary_terms", ["first_course_key"])

    op.create_table(
        "vocabulary_term_relations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("term_id", sa.Integer(), sa.ForeignKey("vocabulary_terms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("related_term_id", sa.Integer(), sa.ForeignKey("vocabulary_terms.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("term_id", "related_term_id", name="uq_vocab_term_relation"),
    )
    op.create_index("ix_vocabulary_term_relations_id", "vocabulary_term_relations", ["id"])
    op.create_index("ix_vocabulary_term_relations_term_id", "vocabulary_term_relations", ["term_id"])
    op.create_index("ix_vocabulary_term_relations_related_term_id", "vocabulary_term_relations", ["related_term_id"])

    op.create_table(
        "vocabulary_term_associations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("term_id", sa.Integer(), sa.ForeignKey("vocabulary_terms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_key", sa.String(20), nullable=False),
        sa.Column("module_key", sa.String(20), nullable=True),
        sa.Column("lesson_key", sa.String(20), nullable=True),
        sa.UniqueConstraint("term_id", "course_key", "module_key", "lesson_key", name="uq_vocab_term_association"),
    )
    op.create_index("ix_vocabulary_term_associations_id", "vocabulary_term_associations", ["id"])
    op.create_index("ix_vocabulary_term_associations_term_id", "vocabulary_term_associations", ["term_id"])
    op.create_index("ix_vocabulary_term_associations_course_key", "vocabulary_term_associations", ["course_key"])

    op.add_column(
        "user_term_progress",
        sa.Column("vocabulary_term_id", sa.Integer(), sa.ForeignKey("vocabulary_terms.id"), nullable=True),
    )
    op.create_index("ix_user_term_progress_vocabulary_term_id", "user_term_progress", ["vocabulary_term_id"])


def downgrade() -> None:
    op.drop_index("ix_user_term_progress_vocabulary_term_id", table_name="user_term_progress")
    op.drop_column("user_term_progress", "vocabulary_term_id")

    op.drop_index("ix_vocabulary_term_associations_course_key", table_name="vocabulary_term_associations")
    op.drop_index("ix_vocabulary_term_associations_term_id", table_name="vocabulary_term_associations")
    op.drop_index("ix_vocabulary_term_associations_id", table_name="vocabulary_term_associations")
    op.drop_table("vocabulary_term_associations")

    op.drop_index("ix_vocabulary_term_relations_related_term_id", table_name="vocabulary_term_relations")
    op.drop_index("ix_vocabulary_term_relations_term_id", table_name="vocabulary_term_relations")
    op.drop_index("ix_vocabulary_term_relations_id", table_name="vocabulary_term_relations")
    op.drop_table("vocabulary_term_relations")

    op.drop_index("ix_vocabulary_terms_first_course_key", table_name="vocabulary_terms")
    op.drop_index("ix_vocabulary_terms_difficulty", table_name="vocabulary_terms")
    op.drop_index("ix_vocabulary_terms_category", table_name="vocabulary_terms")
    op.drop_index("ix_vocabulary_terms_slug", table_name="vocabulary_terms")
    op.drop_index("ix_vocabulary_terms_id", table_name="vocabulary_terms")
    op.drop_table("vocabulary_terms")
