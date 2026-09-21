"""record which Terms of Service and Privacy Policy an account accepted

Four nullable columns on `users`: the version and the time of each acceptance.
Storing only "accepted = true" would not say *what* was accepted, and once a
document changes that is the only question that matters.

Existing accounts are NOT backfilled. They never saw these documents, so their
columns stay NULL, which the API reports as "acceptance required": they are
asked to accept the current versions the next time they use the app. Marking
them as having accepted anything would be inventing consent.

Revision ID: 014_legal_acceptance
Revises: 013_learner_skills
Create Date: 2026-09-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '014_legal_acceptance'
down_revision: Union[str, None] = '013_learner_skills'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('terms_version', sa.String(), nullable=True))
    op.add_column('users', sa.Column('terms_accepted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('privacy_version', sa.String(), nullable=True))
    op.add_column('users', sa.Column('privacy_accepted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'privacy_accepted_at')
    op.drop_column('users', 'privacy_version')
    op.drop_column('users', 'terms_accepted_at')
    op.drop_column('users', 'terms_version')
