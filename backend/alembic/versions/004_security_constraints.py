"""security constraints

Database-level guarantees for things the application already tries to
enforce. The point of putting them here rather than only in Python is
that a migration, a seed script, a psql session or a future endpoint
cannot bypass them the way they can bypass a controller check.

1. users.role NOT NULL DEFAULT 'student' — role was nullable, so a row
   could exist with no role at all. Every authorization decision reads
   this column; "no role" is an ambiguous state that authz code has to
   guess about, and a guess in an authz path is how fail-open bugs start.

2. Case-insensitive uniqueness on users.email — the API now normalizes
   addresses to lowercase, but the existing unique index is
   case-sensitive, so any row written before this (or by a seed script)
   could still collide as Alice@x.com vs alice@x.com. A functional unique
   index on lower(email) makes duplicates impossible regardless of what
   wrote them.

3. CHECK constraints on wallet balances — credits are money-adjacent.
   A negative balance or a negative lifetime total is always a bug, and
   the database is the right place to refuse to store one.

Revision ID: 004_security_constraints
Revises: 003_answer_submissions
Create Date: 2026-09-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '004_security_constraints'
down_revision: Union[str, None] = '003_answer_submissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. users.role ─────────────────────────────────────────────────────
    op.execute("UPDATE users SET role = 'student' WHERE role IS NULL")
    op.alter_column(
        'users', 'role',
        existing_type=sa.Enum('student', 'mentor', 'admin', name='userrole'),
        nullable=False,
        server_default='student',
    )

    # ── 2. case-insensitive email uniqueness ──────────────────────────────
    # Fold any addresses that only differ by case before adding the index,
    # otherwise the CREATE fails on pre-existing data. Rows that would
    # collide keep the oldest account and get their duplicates suffixed
    # so nothing is silently destroyed; operators can then merge manually.
    op.execute("""
        WITH ranked AS (
            SELECT id,
                   row_number() OVER (PARTITION BY lower(email) ORDER BY id) AS rn
            FROM users
        )
        UPDATE users u
        SET email = u.email || '.dup' || r.rn
        FROM ranked r
        WHERE u.id = r.id AND r.rn > 1
    """)
    op.execute("UPDATE users SET email = lower(email) WHERE email <> lower(email)")
    op.execute("CREATE UNIQUE INDEX ix_users_email_lower ON users (lower(email))")

    # ── 3. wallet invariants ──────────────────────────────────────────────
    op.execute("UPDATE user_wallets SET credit_balance = 0 WHERE credit_balance < 0")
    op.create_check_constraint(
        'ck_user_wallets_balance_non_negative', 'user_wallets', 'credit_balance >= 0',
    )
    op.create_check_constraint(
        'ck_user_wallets_lifetime_non_negative', 'user_wallets',
        'lifetime_purchased >= 0 AND lifetime_spent >= 0',
    )

    # ── 4. one email token row per hash is already unique; add the lookup
    # index the expiry sweep will need.
    op.create_index(
        'ix_email_tokens_user_purpose', 'email_tokens', ['user_id', 'purpose'], unique=False,
    )


def downgrade() -> None:
    op.drop_index('ix_email_tokens_user_purpose', table_name='email_tokens')
    op.drop_constraint('ck_user_wallets_lifetime_non_negative', 'user_wallets', type_='check')
    op.drop_constraint('ck_user_wallets_balance_non_negative', 'user_wallets', type_='check')
    op.execute("DROP INDEX IF EXISTS ix_users_email_lower")
    op.alter_column(
        'users', 'role',
        existing_type=sa.Enum('student', 'mentor', 'admin', name='userrole'),
        nullable=True,
        server_default=None,
    )
