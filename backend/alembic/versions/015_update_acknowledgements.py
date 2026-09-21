"""record which product announcements an account has seen

One row per (account, announcement). A table rather than a column per feature
because the next announcement should not need a migration, and the unique
constraint is what makes acknowledging idempotent.

Existing accounts are NOT backfilled: they have not seen the announcement, and
having no row is exactly what makes the API report it as pending. New accounts
get their row from registration.

Revision ID: 015_update_acknowledgements
Revises: 014_legal_acceptance
Create Date: 2026-09-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '015_update_acknowledgements'
down_revision: Union[str, None] = '014_legal_acceptance'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_update_acknowledgements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('release_id', sa.String(length=64), nullable=False),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('user_id', 'release_id', name='uq_user_update_ack'),
    )
    op.create_index('ix_user_update_acknowledgements_user_id', 'user_update_acknowledgements', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_update_acknowledgements_user_id', table_name='user_update_acknowledgements')
    op.drop_table('user_update_acknowledgements')
