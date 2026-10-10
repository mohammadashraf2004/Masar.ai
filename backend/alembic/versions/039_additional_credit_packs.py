"""Additional AI credit packs: the server-owned catalogue, a purchased-credit
bucket, and the ledger links purchases, reversals and refunds need.

Additive only. Nothing here rewrites a balance a learner already has:

* ``credit_packages`` gains a stable ``code`` and ``sort_order`` and the four
  launch packs are upserted by code (Starter 50 / 29 EGP, Standard 150 / 69,
  Plus 400 / 149 - the popular one, Power 1,000 / 299). Packs that carry no code
  are the old seed's and are switched off, never deleted: nothing links to them.
* ``user_wallets.purchased_credits`` is the part of ``credit_balance`` that was
  bought. It is backfilled as ``LEAST(credit_balance, lifetime_purchased)``: a
  buyer never ends up with less purchased credit than they paid for (within what
  they still hold), and a wallet that never bought anything stays at 0.
* ``wallet_transactions`` gains the columns that make each row traceable:
  ``package_id`` (which pack an order bought), ``purchased_delta`` (how much of
  the row moved in or out of the purchased bucket), ``related_tx_id`` (the row a
  refund or reversal answers), ``reversed_credits`` (how much of an order has been
  reversed so far) and ``settled_at`` (when a payment was confirmed).
* the ``transactiontype`` enum gains ``reversal``, the row written when a refund
  or chargeback takes purchased credits back.

Revision ID: 039_additional_credit_packs
Revises: 038_pro_ai_release_reason
Create Date: 2026-10-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "039_additional_credit_packs"
down_revision: Union[str, None] = "038_pro_ai_release_reason"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# (code, name, credits, EGP price, popular, sort order)
PACKS = [
    ("starter", "Starter", 50, 29.0, False, 1),
    ("standard", "Standard", 150, 69.0, False, 2),
    ("plus", "Plus", 400, 149.0, True, 3),
    ("power", "Power", 1000, 299.0, False, 4),
]


def _columns(table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    # ── The enum value must be committed before any row may use it. ──────
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'reversal'")

    # ── Catalogue ─────────────────────────────────────────────────────────
    if "code" not in _columns("credit_packages"):
        op.add_column("credit_packages", sa.Column("code", sa.String(length=32), nullable=True))
        op.add_column("credit_packages", sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"))
        op.create_index("uq_credit_packages_code", "credit_packages", ["code"], unique=True)

    bind = op.get_bind()
    # The old seed's packs (no code) stop being sold; their rows stay.
    bind.execute(sa.text("UPDATE credit_packages SET is_active = false WHERE code IS NULL"))
    for code, name, credits, price, popular, order in PACKS:
        bind.execute(sa.text(
            "INSERT INTO credit_packages (code, name, credits, egp_price, bonus_credits, is_active, is_popular, "
            "description, sort_order) VALUES (:code, :name, :credits, :price, 0, true, :popular, :description, :order) "
            "ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name, credits = EXCLUDED.credits, "
            "egp_price = EXCLUDED.egp_price, bonus_credits = 0, is_active = true, is_popular = EXCLUDED.is_popular, "
            "sort_order = EXCLUDED.sort_order"
        ), {
            "code": code, "name": name, "credits": credits, "price": price, "popular": popular, "order": order,
            "description": f"{credits:,} AI credits that never expire.",
        })

    # ── Wallet: the purchased bucket ──────────────────────────────────────
    if "purchased_credits" not in _columns("user_wallets"):
        op.add_column("user_wallets", sa.Column("purchased_credits", sa.Integer(), nullable=False, server_default="0"))
        bind.execute(sa.text(
            "UPDATE user_wallets SET purchased_credits = GREATEST(0, LEAST(COALESCE(credit_balance, 0), "
            "COALESCE(lifetime_purchased, 0)))"
        ))
        op.create_check_constraint("ck_user_wallets_purchased_non_negative", "user_wallets", "purchased_credits >= 0")

    # ── Ledger links ──────────────────────────────────────────────────────
    existing = _columns("wallet_transactions")
    additions = [
        ("package_id", sa.Column("package_id", sa.Integer(), nullable=True)),
        ("purchased_delta", sa.Column("purchased_delta", sa.Integer(), nullable=False, server_default="0")),
        ("related_tx_id", sa.Column("related_tx_id", sa.Integer(), nullable=True)),
        ("reversed_credits", sa.Column("reversed_credits", sa.Integer(), nullable=False, server_default="0")),
        ("settled_at", sa.Column("settled_at", sa.DateTime(timezone=True), nullable=True)),
        ("request_key", sa.Column("request_key", sa.String(length=160), nullable=True)),
    ]
    for name, column in additions:
        if name not in existing:
            op.add_column("wallet_transactions", column)
    # Every confirmed payment already made keeps a settle time: its own creation time.
    bind.execute(sa.text(
        "UPDATE wallet_transactions SET settled_at = created_at "
        "WHERE settled_at IS NULL AND transaction_type = 'topup' AND status = 'confirmed'"
    ))
    # Confirmed top-ups already in the ledger bought purchased credits.
    bind.execute(sa.text(
        "UPDATE wallet_transactions SET purchased_delta = credits "
        "WHERE transaction_type = 'topup' AND status = 'confirmed' AND purchased_delta = 0"
    ))
    op.create_index("ix_wallet_transactions_related_tx_id", "wallet_transactions", ["related_tx_id"], unique=False)
    op.create_index(
        "ix_wallet_transactions_request_key", "wallet_transactions", ["wallet_id", "request_key"], unique=False,
        postgresql_where=sa.text("request_key IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_wallet_transactions_request_key", table_name="wallet_transactions")
    op.drop_index("ix_wallet_transactions_related_tx_id", table_name="wallet_transactions")
    for name in ("request_key", "settled_at", "reversed_credits", "related_tx_id", "purchased_delta", "package_id"):
        op.drop_column("wallet_transactions", name)
    op.drop_constraint("ck_user_wallets_purchased_non_negative", "user_wallets", type_="check")
    op.drop_column("user_wallets", "purchased_credits")
    op.drop_index("uq_credit_packages_code", table_name="credit_packages")
    op.drop_column("credit_packages", "sort_order")
    op.drop_column("credit_packages", "code")
    # PostgreSQL cannot remove an enum value; 'reversal' stays, unused. The four
    # packs and the deactivation of the old seed's packs are catalogue data, left as they are.
