"""launch promo credits

Tracks the launch-promotion credit bundle separately from the rest of a
wallet's balance, so that when a user's promo window closes we can
withdraw only the credits they did NOT spend and never touch credits they
paid for.

Both columns are server-set. No request schema exposes either, so a
client cannot extend its own promo window or mint credits.

Revision ID: 005_launch_promo_credits
Revises: 004_security_constraints
Create Date: 2026-09-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '005_launch_promo_credits'
down_revision: Union[str, None] = '004_security_constraints'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'user_wallets',
        sa.Column('promo_credits_remaining', sa.Integer(), nullable=False, server_default='0'),
    )
    op.add_column(
        'user_wallets',
        sa.Column('promo_expires_at', sa.DateTime(timezone=True), nullable=True),
    )
    # Same reasoning as the existing wallet CHECKs in 004: promo credits
    # are money-adjacent, and a negative remainder is always a bug.
    op.create_check_constraint(
        'ck_user_wallets_promo_non_negative', 'user_wallets', 'promo_credits_remaining >= 0',
    )
    # The expiry sweep is lazy (runs when a wallet is touched), but an
    # operator reporting on outstanding promo liability will scan on this.
    op.create_index(
        'ix_user_wallets_promo_expires_at', 'user_wallets', ['promo_expires_at'], unique=False,
    )

    # The enum gains a value for the withdrawal transaction, so promo
    # expiry shows up in the ledger rather than as a silent balance change.
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'expiry'")


def downgrade() -> None:
    op.drop_index('ix_user_wallets_promo_expires_at', table_name='user_wallets')
    op.drop_constraint('ck_user_wallets_promo_non_negative', 'user_wallets', type_='check')
    op.drop_column('user_wallets', 'promo_expires_at')
    op.drop_column('user_wallets', 'promo_credits_remaining')
    # PostgreSQL cannot remove a value from an enum type; 'expiry' is left
    # in place. Harmless — nothing writes it once the columns are gone.
