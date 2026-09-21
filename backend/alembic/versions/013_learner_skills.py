"""learner skills, and telling a skill from a tool

Personalised roadmaps need to know what a learner already knows. The profile
already carried a JSON list of skill slugs, but a list cannot say *how* we know
a skill (the learner said so, they passed an assessment, they finished a
course) or how sure we are - and "known" must never be read as "mastered".

`learner_skills` is one row per (learner, skill) with a `status`
(known / learning / mastered) and a `source` (self_declared / assessment /
course_completion). Onboarding writes known + self_declared. Better evidence
later upgrades the same row; nothing here has to change.

Also adds `skills.kind` ('skill' | 'tool'), because "RAG" and "LangChain" are
different kinds of thing and selecting the tool must not read as having the
skill. Existing rows default to 'skill'; the tools the current catalogue names
are tagged by slug below (a slug is the stable identity, so this is safe on any
database, and a slug that is absent simply matches nothing).

The old `learning_profiles.known_skill_slugs` values are copied across
(self_declared, known) and the column is left in place, unused: nothing is
destroyed and the migration is reversible.

Revision ID: 013_learner_skills
Revises: 012_learning_profile_backfill
Create Date: 2026-09-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '013_learner_skills'
down_revision: Union[str, None] = '012_learning_profile_backfill'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Frozen snapshot, like the vocabulary in 011: a migration must not change
# meaning when the seed later evolves.
_TOOL_SLUGS = ("langchain", "langgraph", "llamaindex", "qdrant", "fastapi")


def upgrade() -> None:
    op.add_column(
        'skills',
        sa.Column('kind', sa.String(), nullable=False, server_default='skill'),
    )
    op.create_check_constraint('ck_skills_kind', 'skills', "kind IN ('skill', 'tool')")

    op.create_table(
        'learner_skills',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='known'),
        sa.Column('source', sa.String(), nullable=False, server_default='self_declared'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.UniqueConstraint('user_id', 'skill_id', name='uq_learner_skills_user_skill'),
        sa.CheckConstraint("status IN ('known', 'learning', 'mastered')", name='ck_learner_skills_status'),
        sa.CheckConstraint(
            "source IN ('self_declared', 'assessment', 'course_completion')", name='ck_learner_skills_source',
        ),
    )
    op.create_index('ix_learner_skills_id', 'learner_skills', ['id'])
    op.create_index('ix_learner_skills_user_id', 'learner_skills', ['user_id'])

    bind = op.get_bind()
    bind.execute(
        sa.text("UPDATE skills SET kind = 'tool' WHERE slug IN :slugs").bindparams(
            sa.bindparam('slugs', expanding=True)
        ),
        {"slugs": list(_TOOL_SLUGS)},
    )
    copy_declared_skills(bind)


def copy_declared_skills(bind) -> int:
    """Copy each profile's `known_skill_slugs` into `learner_skills` as
    (known, self_declared). Slugs that no longer name a skill are dropped
    (nothing to point at) and duplicates collapse to one row. Idempotent.
    Returns how many rows were written."""
    import json

    rows = bind.execute(
        sa.text("SELECT user_id, known_skill_slugs FROM learning_profiles")
    ).fetchall()
    skill_id = {slug: sid for sid, slug in bind.execute(sa.text("SELECT id, slug FROM skills")).fetchall()}
    written = 0
    for user_id, slugs in rows:
        if isinstance(slugs, str):  # a JSON column can come back as text on some drivers
            slugs = json.loads(slugs)
        for slug in dict.fromkeys(slugs or []):
            sid = skill_id.get(slug)
            if sid is None:
                continue
            result = bind.execute(
                sa.text(
                    "INSERT INTO learner_skills (user_id, skill_id, status, source) "
                    "VALUES (:u, :s, 'known', 'self_declared') "
                    "ON CONFLICT ON CONSTRAINT uq_learner_skills_user_skill DO NOTHING"
                ),
                {"u": user_id, "s": sid},
            )
            written += result.rowcount or 0
    return written


def downgrade() -> None:
    op.drop_index('ix_learner_skills_user_id', table_name='learner_skills')
    op.drop_index('ix_learner_skills_id', table_name='learner_skills')
    op.drop_table('learner_skills')
    op.drop_constraint('ck_skills_kind', 'skills', type_='check')
    op.drop_column('skills', 'kind')
