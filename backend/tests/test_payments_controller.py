"""
End-to-end test of the webhook endpoint itself: a pending WalletTransaction
gets created, a correctly-signed webhook confirms it and releases credits,
and a wrongly-signed one is rejected and changes nothing.
"""
import hashlib
import hmac as hmac_lib
import uuid

from app.db.session import SessionLocal
from app.models.user import User
from app.models.wallet import UserWallet, WalletTransaction, TransactionStatus, TransactionType, PaymentMethod
from app.core.security import get_password_hash
from app.services.wallet.wallet_service import get_or_create_wallet
from app.services.payments import paymob_service

SECRET = "test-webhook-secret"


def _sign(secret: str, obj: dict) -> str:
    concatenated = "".join(
        paymob_service._stringify(paymob_service._extract(obj, f))
        for f in paymob_service._HMAC_FIELDS
    )
    return hmac_lib.new(secret.encode(), concatenated.encode(), hashlib.sha512).hexdigest()


def _make_pending_topup(db, credits=100, egp=50.0):
    email = f"webhook-{uuid.uuid4().hex[:12]}@example.com"
    user = User(email=email, full_name="Webhook Test", hashed_password=get_password_hash("x"))
    db.add(user)
    db.commit()
    db.refresh(user)

    wallet = get_or_create_wallet(user.id, db)
    merchant_order_id = f"wallet-{uuid.uuid4().hex}"
    tx = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.topup,
        status=TransactionStatus.pending,
        credits=credits,
        egp_amount=egp,
        payment_method=PaymentMethod.card,
        payment_ref=merchant_order_id,
        description="test package",
        balance_after=wallet.credit_balance,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return user, wallet, tx, merchant_order_id


def _webhook_obj(merchant_order_id: str, success: bool = True) -> dict:
    return {
        "amount_cents": 5000,
        "created_at": "2026-08-20T10:00:00.000000",
        "currency": "EGP",
        "error_occured": False,
        "has_parent_transaction": False,
        "id": 1,
        "integration_id": 1,
        "is_3d_secure": True,
        "is_auth": False,
        "is_capture": False,
        "is_refunded": False,
        "is_standalone_payment": True,
        "is_voided": False,
        "order": {"id": 1, "merchant_order_id": merchant_order_id},
        "owner": 1,
        "pending": False,
        "source_data": {"pan": "1234", "sub_type": "MasterCard", "type": "card"},
        "success": success,
    }


def test_webhook_confirms_pending_topup_and_releases_credits(client, monkeypatch, db):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)

    setup = SessionLocal()
    user, wallet, tx, merchant_order_id = _make_pending_topup(setup)
    user_id, wallet_id = user.id, wallet.id
    setup.close()

    obj = _webhook_obj(merchant_order_id)
    signature = _sign(SECRET, obj)

    resp = client.post(f"/api/v1/payments/paymob/webhook?hmac={signature}", json={"type": "TRANSACTION", "obj": obj})
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    check = SessionLocal()
    updated_tx = check.query(WalletTransaction).filter(WalletTransaction.payment_ref == merchant_order_id).first()
    updated_wallet = check.query(UserWallet).filter(UserWallet.id == wallet_id).first()
    assert updated_tx.status == TransactionStatus.confirmed
    assert updated_wallet.credit_balance == 100

    check.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet_id).delete()
    check.query(UserWallet).filter(UserWallet.id == wallet_id).delete()
    check.query(User).filter(User.id == user_id).delete()
    check.commit()
    check.close()


def test_webhook_with_bad_signature_is_rejected_and_changes_nothing(client, monkeypatch, db):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)

    setup = SessionLocal()
    user, wallet, tx, merchant_order_id = _make_pending_topup(setup)
    user_id, wallet_id = user.id, wallet.id
    setup.close()

    obj = _webhook_obj(merchant_order_id)

    resp = client.post("/api/v1/payments/paymob/webhook?hmac=not-the-real-signature", json={"type": "TRANSACTION", "obj": obj})
    assert resp.status_code == 401

    check = SessionLocal()
    updated_tx = check.query(WalletTransaction).filter(WalletTransaction.payment_ref == merchant_order_id).first()
    updated_wallet = check.query(UserWallet).filter(UserWallet.id == wallet_id).first()
    assert updated_tx.status == TransactionStatus.pending  # untouched
    assert updated_wallet.credit_balance == 0               # untouched

    check.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet_id).delete()
    check.query(UserWallet).filter(UserWallet.id == wallet_id).delete()
    check.query(User).filter(User.id == user_id).delete()
    check.commit()
    check.close()
