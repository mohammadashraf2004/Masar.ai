"""
Migration 039 (additional credit packs) on a database that already holds wallets.

Downgrades the test database to 038, plants the rows a live database would have, upgrades
again and checks that nothing a learner holds is rewritten, the purchased bucket is
backfilled safely and the four launch packs are the only ones on sale.
"""
import uuid

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config

import app.main  # noqa: F401
from app.core.security import get_password_hash
from app.db.session import SessionLocal, engine
from app.models.user import User


def _config():
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", engine.url.render_as_string(hide_password=False))
    return cfg


@pytest.fixture()
def at_038():
    command.downgrade(_config(), "038_pro_ai_release_reason")
    try:
        yield
    finally:
        command.upgrade(_config(), "head")


def test_039_backfills_the_purchased_bucket_and_replaces_the_catalogue_without_touching_balances(at_038):
    session = SessionLocal()
    users = []
    for i in range(5):
        user = User(email=f"mig039-{uuid.uuid4().hex[:8]}-{i}@example.com", full_name="Mig", hashed_password=get_password_hash("x"))
        session.add(user)
        session.flush()
        users.append(user.id)
    session.commit()
    # balance / lifetime_purchased, and what the ledger says was really bought:
    #   0  a buyer who still holds more than they bought
    #   1  a buyer who spent most of it
    #   2  a learner who never bought anything (an unpaid top-up does not count)
    #   3  PRODUCTION'S SHAPE: a launch-promo account. The promo was recorded in lifetime_purchased
    #      (500), but the ledger holds only a bonus row, so nothing was bought.
    #   4  two confirmed top-ups plus a bonus: only the top-ups are purchases
    shapes = [(100, 60), (20, 60), (30, 0), (500, 500), (150, 100)]
    with engine.begin() as conn:
        wallets = []
        for uid, (balance, bought) in zip(users, shapes):
            wallets.append(conn.execute(sa.text(
                "INSERT INTO user_wallets (user_id, credit_balance, lifetime_purchased, lifetime_spent) "
                "VALUES (:u, :b, :p, 0) RETURNING id"), {"u": uid, "b": balance, "p": bought}).scalar())

        def ledger(wallet, kind, status, credits, description, balance_after, paid=True):
            conn.execute(sa.text(
                "INSERT INTO wallet_transactions (wallet_id, transaction_type, status, credits, egp_amount, payment_ref, "
                "description, balance_after) VALUES (:w, CAST(:k AS transactiontype), CAST(:s AS transactionstatus), "
                ":c, :egp, :ref, :d, :after)"),
                {"w": wallet, "k": kind, "s": status, "c": credits, "egp": 30.0 if paid else None,
                 "ref": f"legacy-{uuid.uuid4().hex[:8]}" if paid else None, "d": description, "after": balance_after})

        ledger(wallets[0], "topup", "confirmed", 60, "old", 100)
        ledger(wallets[1], "topup", "confirmed", 60, "old-spent", 20)
        ledger(wallets[2], "topup", "pending", 70, "unpaid", 30)
        ledger(wallets[3], "bonus", "confirmed", 500, "Launch promo - 500 free credits", 500, paid=False)
        ledger(wallets[4], "topup", "confirmed", 40, "old-a", 40)
        ledger(wallets[4], "topup", "confirmed", 60, "old-b", 100)
        ledger(wallets[4], "bonus", "confirmed", 50, "bonus-extra", 150, paid=False)
        conn.execute(sa.text(
            "INSERT INTO credit_packages (name, credits, egp_price, bonus_credits, is_active, is_popular) "
            "VALUES ('OldSeed', 999, 1.0, 0, true, true)"))

    command.upgrade(_config(), "head")

    with engine.connect() as conn:
        rows = {r.user_id: r for r in conn.execute(sa.text(
            "SELECT user_id, credit_balance, purchased_credits, lifetime_purchased FROM user_wallets WHERE user_id = ANY(:ids)"),
            {"ids": users})}
        # balances are exactly what they were; the bucket is what the LEDGER shows they bought, capped at
        # what they hold. The promo account (lifetime_purchased 500) has bought nothing: its promo must stay
        # expirable, so its purchased bucket is 0.
        assert [(rows[u].credit_balance, rows[u].purchased_credits) for u in users] == [
            (100, 60), (20, 20), (30, 0), (500, 0), (150, 100)]
        assert rows[users[3]].lifetime_purchased == 500        # the counter itself is left exactly as it was
        confirmed = conn.execute(sa.text(
            "SELECT purchased_delta, settled_at FROM wallet_transactions WHERE description = 'old'")).one()
        assert confirmed.purchased_delta == 60 and confirmed.settled_at is not None
        unpaid = conn.execute(sa.text(
            "SELECT purchased_delta, settled_at FROM wallet_transactions WHERE description = 'unpaid'")).one()
        assert unpaid.purchased_delta == 0 and unpaid.settled_at is None

        sold = conn.execute(sa.text(
            "SELECT code, credits, egp_price, is_popular FROM credit_packages WHERE is_active ORDER BY sort_order")).all()
        assert [tuple(r) for r in sold] == [
            ("starter", 50, 29.0, False), ("standard", 150, 69.0, False), ("plus", 400, 149.0, True), ("power", 1000, 299.0, False)]
        old = conn.execute(sa.text("SELECT is_active FROM credit_packages WHERE name = 'OldSeed'")).scalar()
        assert old is False                                  # switched off, never deleted

        with pytest.raises(sa.exc.IntegrityError):
            conn.execute(sa.text("UPDATE user_wallets SET purchased_credits = -1 WHERE user_id = :u"), {"u": users[0]})
    session.close()


def test_039_upgrade_is_idempotent_on_the_catalogue(at_038):
    command.upgrade(_config(), "head")
    command.downgrade(_config(), "038_pro_ai_release_reason")
    command.upgrade(_config(), "head")
    with engine.connect() as conn:
        assert conn.execute(sa.text("SELECT count(*) FROM credit_packages WHERE code IS NOT NULL")).scalar() == 4
