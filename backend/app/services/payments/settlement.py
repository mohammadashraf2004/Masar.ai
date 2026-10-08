"""Settle a verified payment notice against whichever order it names.

The one authoritative path for every kind of payment: provider webhooks build a
PaymentNotice from a callback whose signature they verified and hand it here.
A browser redirect never reaches this module. Each kind finds only its own rows,
and a notice settles a row only when the provider order bound at checkout, the
amount and the currency all match; one provider transaction settles at most one
row.
"""
import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core import security_log
from app.models.challenge import ExamPayment
from app.models.wallet import TransactionStatus, UserWallet, WalletTransaction
from app.services.billing.course_billing import settle_course_notice
from app.services.billing.subscriptions import settle_subscription_notice
from app.services.payments.notice import PaymentNotice
from app.services.wallet.wallet_service import confirm_pending_topup

logger = logging.getLogger("app.payments")


def _binding_problem(notice: PaymentNotice, provider_order_id, egp_amount) -> Optional[str]:
    """Why this notice may not settle this row, or None if it may. Rows created
    before migration 034 carry no provider order id and are left for manual
    confirmation rather than trusted on the merchant order id alone."""
    if not notice.event_id:
        return "missing_transaction_id"
    if provider_order_id is None:
        return "unbound_legacy_order"
    if not notice.binds(provider_order_id):
        return "provider_order_mismatch"
    if notice.amount < 0 or egp_amount is None or notice.amount != round(float(egp_amount) * 100):
        return "amount_mismatch"
    if notice.currency != "EGP":
        return "currency_mismatch"
    return None


def settle_wallet_topup(db: Session, notice: PaymentNotice) -> Optional[dict]:
    tx = (
        db.query(WalletTransaction)
        .filter(WalletTransaction.payment_ref == notice.merchant_order_id,
                WalletTransaction.status == TransactionStatus.pending)
        .with_for_update()
        .first()
    )
    if not tx:
        return None
    ref = notice.merchant_order_id
    wallet = db.query(UserWallet).filter(UserWallet.id == tx.wallet_id).one()
    problem = _binding_problem(notice, tx.provider_order_id, tx.egp_amount)
    if problem:
        db.rollback()
        security_log.payment_event(kind=f"wallet_topup_{problem}", ref=ref, success=False, user_id=wallet.user_id)
        return {"status": "rejected", "kind": "wallet_topup", "success": False}
    if not notice.settles:
        # A refund/void/authorization never settles a top-up, and a decline is
        # not final: the buyer can retry inside the same checkout while it lives,
        # and that charge must still find this row pending. Leave it untouched.
        db.rollback()
        security_log.payment_event(kind="wallet_topup_not_settled", ref=ref, success=False, user_id=wallet.user_id)
        return {"status": "processed", "kind": "wallet_topup", "success": False}
    tx.provider_transaction_id = notice.event_id
    try:
        # One authoritative payout path, shared with the admin/manual
        # confirmation in wallet_controller. It takes the wallet row lock itself
        # and is a no-op on an already-confirmed row, so a webhook retry cannot
        # pay the same top-up out twice.
        wallet = confirm_pending_topup(tx, db)
    except IntegrityError:
        # uq_wallet_transactions_provider_txn: this transaction already settled another top-up.
        db.rollback()
        security_log.payment_event(kind="wallet_topup_txn_reused", ref=ref, success=False, user_id=wallet.user_id)
        return {"status": "rejected", "kind": "wallet_topup", "success": False}
    security_log.payment_event(kind="wallet_topup", ref=ref, success=True, user_id=wallet.user_id)
    return {"status": "processed", "kind": "wallet_topup", "success": True}


def settle_exam_payment(db: Session, notice: PaymentNotice) -> Optional[dict]:
    payment = (
        db.query(ExamPayment)
        .filter(ExamPayment.payment_ref == notice.merchant_order_id, ExamPayment.status == "pending")
        .with_for_update()
        .first()
    )
    if not payment:
        return None
    ref = notice.merchant_order_id
    problem = _binding_problem(notice, payment.provider_order_id, payment.egp_amount)
    if problem:
        db.rollback()
        security_log.payment_event(kind=f"exam_payment_{problem}", ref=ref, success=False, user_id=payment.user_id)
        return {"status": "rejected", "kind": "exam_payment", "success": False}
    if not notice.settles:
        # Same rule as top-ups: a decline is not final while the buyer can still
        # retry inside this checkout, so the row stays pending.
        db.rollback()
        security_log.payment_event(kind="exam_payment_not_settled", ref=ref, success=False, user_id=payment.user_id)
        return {"status": "processed", "kind": "exam_payment", "success": False}
    payment.provider_transaction_id = notice.event_id
    payment.status = "confirmed"
    payment.confirmed_by = "webhook"
    payment.confirmed_at = datetime.now(timezone.utc)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        security_log.payment_event(kind="exam_payment_txn_reused", ref=ref, success=False, user_id=payment.user_id)
        return {"status": "rejected", "kind": "exam_payment", "success": False}
    security_log.payment_event(kind="exam_payment", ref=ref, success=True, user_id=payment.user_id)
    return {"status": "processed", "kind": "exam_payment", "success": True}


def settle_notice(db: Session, notice: PaymentNotice) -> dict:
    """Settle `notice` against the order it names. Raises ValueError for a notice
    that names a subscription or course order but carries no transaction id."""
    for settle in (settle_subscription_notice, settle_course_notice, settle_wallet_topup, settle_exam_payment):
        result = settle(db, notice)
        if result is not None:
            return result
    # Nothing pending matches: acknowledge (so the provider stops retrying an
    # already-processed or unrelated notification) without pretending anything happened.
    return {"status": "no matching pending transaction"}
