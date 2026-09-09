"""
One authoritative credit payout path.

Releasing the credits on a pending top-up was written out inline in two
places — the Paymob webhook and the admin/manual confirmation — as the
same four lines:

    wallet.credit_balance     += tx.credits
    wallet.lifetime_purchased += tx.credits
    tx.status = confirmed
    tx.balance_after = wallet.credit_balance

Both now call wallet_service.confirm_pending_topup(). These tests pin the
properties that made centralising it worth doing, rather than just
asserting the refactor happened:

  * both paths pay out identically,
  * neither pays out twice (Paymob retries webhooks),
  * the payout is not expressible as add_credits() — that would insert a
    second transaction row and double-count the purchase in the history.
"""
import uuid

import pytest

from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.wallet import (
    PaymentMethod,
    TransactionStatus,
    TransactionType,
    UserWallet,
    WalletTransaction,
)
from app.services.wallet.wallet_service import confirm_pending_topup, get_or_create_wallet


def _user(db, prefix="topup"):
    user = User(
        email=f"{prefix}-{uuid.uuid4().hex[:12]}@example.com",
        full_name="Topup Tester",
        hashed_password=get_password_hash("x"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _pending_topup(db, user, credits=100, egp=50.0):
    wallet = get_or_create_wallet(user.id, db)
    ref = f"wallet-{uuid.uuid4().hex}"
    tx = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.topup,
        status=TransactionStatus.pending,
        credits=credits,
        egp_amount=egp,
        payment_method=PaymentMethod.card,
        payment_ref=ref,
        description="test package",
        balance_after=wallet.credit_balance,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return wallet, tx, ref


def test_confirming_releases_the_credits(db):
    user = _user(db)
    wallet, tx, _ = _pending_topup(db, user, credits=100)
    before = wallet.credit_balance

    confirm_pending_topup(tx, db)

    db.expire_all()
    wallet = db.query(UserWallet).filter(UserWallet.id == wallet.id).one()
    assert wallet.credit_balance == before + 100
    assert wallet.lifetime_purchased == 100
    assert tx.status == TransactionStatus.confirmed
    assert tx.balance_after == wallet.credit_balance


def test_confirming_twice_pays_out_once(db):
    """Paymob retries webhooks. A retry that lands after the first one
    committed must not top the user up again."""
    user = _user(db)
    wallet, tx, _ = _pending_topup(db, user, credits=100)
    before = wallet.credit_balance

    confirm_pending_topup(tx, db)
    confirm_pending_topup(tx, db)
    confirm_pending_topup(tx, db)

    db.expire_all()
    wallet = db.query(UserWallet).filter(UserWallet.id == wallet.id).one()
    assert wallet.credit_balance == before + 100, "a repeated confirmation paid out twice"
    assert wallet.lifetime_purchased == 100


def test_confirming_does_not_add_a_second_transaction_row(db):
    """Why this is not add_credits(): the pending row already exists, and
    inserting another would report one purchase as two in the wallet
    history the user reads."""
    user = _user(db)
    wallet, tx, _ = _pending_topup(db, user, credits=100)
    before = db.query(WalletTransaction).filter(
        WalletTransaction.wallet_id == wallet.id,
    ).count()

    confirm_pending_topup(tx, db)

    after = db.query(WalletTransaction).filter(
        WalletTransaction.wallet_id == wallet.id,
    ).count()
    assert after == before


def test_a_failed_topup_pays_out_nothing(db):
    user = _user(db)
    wallet, tx, _ = _pending_topup(db, user, credits=100)
    before = wallet.credit_balance

    tx.status = TransactionStatus.failed
    db.commit()
    confirm_pending_topup(tx, db)

    db.expire_all()
    wallet = db.query(UserWallet).filter(UserWallet.id == wallet.id).one()
    assert wallet.credit_balance == before, "a failed top-up released credits"


def test_admin_confirm_endpoint_uses_the_same_path(client, db):
    """The manual/Fawry confirmation route, end to end."""
    user = _user(db, "adminconfirm")
    wallet, tx, ref = _pending_topup(db, user, credits=250)
    before = wallet.credit_balance

    admin = _user(db, "admin")
    db.query(User).filter(User.id == admin.id).update({User.role: UserRole.admin})
    db.commit()

    from app.core.security import create_access_token_for_user

    db.refresh(admin)
    token = create_access_token_for_user(admin)

    resp = client.post(
        f"/api/v1/wallet/admin/confirm/{ref}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["credits_added"] == 250

    db.expire_all()
    wallet = db.query(UserWallet).filter(UserWallet.id == wallet.id).one()
    assert wallet.credit_balance == before + 250

    # And a second confirmation of the same reference finds nothing
    # pending, so it cannot double-pay through the endpoint either.
    again = client.post(
        f"/api/v1/wallet/admin/confirm/{ref}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert again.status_code == 404

    db.expire_all()
    wallet = db.query(UserWallet).filter(UserWallet.id == wallet.id).one()
    assert wallet.credit_balance == before + 250


def test_no_controller_mutates_a_wallet_balance_directly(db):
    """The invariant this whole priority was about.

    Credit arithmetic belongs to wallet_service, where the row lock, the
    promo-expiry check, the spend metric and the transaction row all live.
    A controller that adjusts a balance inline silently skips every one of
    them. This is a grep, deliberately: it fails when someone reintroduces
    the pattern, which no behavioural test would catch.
    """
    import pathlib
    import re

    controllers = pathlib.Path("app/controllers")
    pattern = re.compile(
        r"\.(credit_balance|lifetime_purchased|lifetime_spent|promo_credits_remaining)"
        r"\s*(\+=|-=|=(?!=))"
    )
    offenders = []
    for path in sorted(controllers.glob("*.py")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                offenders.append(f"{path}:{lineno}: {line.strip()}")

    assert not offenders, (
        "controllers must go through app.services.wallet.wallet_service, not "
        "adjust wallet fields inline:\n  " + "\n  ".join(offenders)
    )
