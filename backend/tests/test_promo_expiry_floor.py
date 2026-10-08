"""
Launch-promo expiry never takes a wallet below the Free plan's 40 credits
(release decision 2026-10-08).

About a hundred pre-launch accounts hold a 500-credit launch promo that lapses
from 2026-10-10. Migration 021 raised only wallets under 40, so without this
floor a lapsed promo wallet would drop to whatever it had besides the promo -
often 0, less than a brand-new signup gets.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.models.user import User
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services.wallet.wallet_service import FREE_PLAN_CREDITS, expire_promo_credits_if_due


@pytest.fixture()
def wallet(db):
    user = User(email=f"promo-floor-{uuid.uuid4().hex[:10]}@example.com", full_name="P", hashed_password="x")
    db.add(user)
    db.flush()
    row = UserWallet(user_id=user.id, credit_balance=0)
    db.add(row)
    db.commit()
    yield row
    db.rollback()
    db.query(WalletTransaction).filter(WalletTransaction.wallet_id == row.id).delete()
    db.query(UserWallet).filter(UserWallet.id == row.id).delete()
    db.query(User).filter(User.id == user.id).delete()
    db.commit()


def _set(db, wallet, balance, promo, lapsed=True):
    wallet.credit_balance = balance
    wallet.promo_credits_remaining = promo
    wallet.promo_expires_at = datetime.now(timezone.utc) + timedelta(days=-1 if lapsed else 1)
    db.commit()


def _expiries(db, wallet):
    return db.query(WalletTransaction).filter(
        WalletTransaction.wallet_id == wallet.id, WalletTransaction.transaction_type == TransactionType.expiry,
    ).all()


def test_an_unspent_promo_lapses_down_to_the_free_plan_not_to_zero(db, wallet):
    _set(db, wallet, balance=500, promo=500)
    assert expire_promo_credits_if_due(wallet, db) == 500 - FREE_PLAN_CREDITS
    db.refresh(wallet)
    assert wallet.credit_balance == FREE_PLAN_CREDITS
    assert wallet.promo_credits_remaining == 0 and wallet.promo_expires_at is None
    [row] = _expiries(db, wallet)
    assert row.credits == -(500 - FREE_PLAN_CREDITS) and row.balance_after == FREE_PLAN_CREDITS


@pytest.mark.parametrize("balance, promo, expected_balance", [
    (40, 40, 40),     # exactly the floor: nothing to take
    (30, 30, 30),     # already under it: nothing taken, never raised either
    (60, 50, 40),     # 10 non-promo + 50 promo: only 20 can go
    (200, 100, 100),  # 100 purchased + 100 promo: all promo goes, purchased stays
    (487, 487, 40),   # the largest real wallet lapsing on launch day
])
def test_expiry_removes_only_promo_above_the_floor(db, wallet, balance, promo, expected_balance):
    _set(db, wallet, balance=balance, promo=promo)
    removed = expire_promo_credits_if_due(wallet, db)
    db.refresh(wallet)
    assert wallet.credit_balance == expected_balance
    assert removed == balance - expected_balance
    assert wallet.promo_credits_remaining == 0 and wallet.promo_expires_at is None
    assert [r.credits for r in _expiries(db, wallet)] == ([-removed] if removed else [])


def test_a_promo_still_in_its_window_is_untouched(db, wallet):
    _set(db, wallet, balance=500, promo=500, lapsed=False)
    assert expire_promo_credits_if_due(wallet, db) == 0
    db.refresh(wallet)
    assert wallet.credit_balance == 500 and wallet.promo_credits_remaining == 500
    assert _expiries(db, wallet) == []


def test_expiry_runs_once(db, wallet):
    _set(db, wallet, balance=500, promo=500)
    expire_promo_credits_if_due(wallet, db)
    assert expire_promo_credits_if_due(wallet, db) == 0
    db.refresh(wallet)
    assert wallet.credit_balance == FREE_PLAN_CREDITS
    assert len(_expiries(db, wallet)) == 1
