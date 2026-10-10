"""Credit-pack purchases: what is for sale, what an order's state is, and how a refund
or chargeback is taken back out of the wallet.

A purchase is a `WalletTransaction` row of type ``topup``. It is created `pending` when
a checkout opens (the price comes from `credit_packages`, never from the request),
bound to the provider's session by `provider_order_id`, and paid out exactly once by
`wallet_service.confirm_pending_topup` - only from a signed, server-confirmed provider
notice (see payments/settlement.py). A later refund or chargeback adds a ``reversal``
row that points back at the order (`related_tx_id`) and takes the credits back out of
the PURCHASED bucket - at most what the wallet still holds there, so a balance can
never go negative; whatever was already spent is recorded as unrecovered.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core import security_log
from app.models.wallet import CreditPackage, TransactionStatus, TransactionType, UserWallet, WalletTransaction

logger = logging.getLogger("app.wallet.purchases")

# A checkout session lives an hour (Kashier `expireAt`); after this an unpaid order can
# no longer be paid and stops counting against the open-order limit.
PENDING_ORDER_TTL = timedelta(minutes=75)
MAX_OPEN_ORDERS = 3

REFUND = "refund"
CHARGEBACK = "chargeback"


def active_packs(db: Session) -> list[CreditPackage]:
    return (
        db.query(CreditPackage).filter(CreditPackage.is_active == True)  # noqa: E712
        .order_by(CreditPackage.sort_order, CreditPackage.id).all()
    )


def is_purchase_order(tx: WalletTransaction) -> bool:
    """A top-up that went through a provider checkout (as opposed to a manual or admin one)."""
    return tx.transaction_type == TransactionType.topup and bool(tx.payment_ref) and str(tx.payment_ref).startswith("wallet-")


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def release_stale_orders(db: Session, wallet_id: int, now: Optional[datetime] = None) -> int:
    """Close this wallet's pending orders that can no longer be paid, so an abandoned
    checkout does not block a new one. The caller commits."""
    now = now or datetime.now(timezone.utc)
    return (
        db.query(WalletTransaction)
        .filter(
            WalletTransaction.wallet_id == wallet_id,
            WalletTransaction.transaction_type == TransactionType.topup,
            WalletTransaction.status == TransactionStatus.pending,
            WalletTransaction.payment_ref.like("wallet-%"),
            WalletTransaction.created_at < now - PENDING_ORDER_TTL,
        )
        .update({WalletTransaction.status: TransactionStatus.failed}, synchronize_session=False)
    )


def open_order_count(db: Session, wallet_id: int, now: Optional[datetime] = None) -> int:
    now = now or datetime.now(timezone.utc)
    return db.query(WalletTransaction.id).filter(
        WalletTransaction.wallet_id == wallet_id,
        WalletTransaction.transaction_type == TransactionType.topup,
        WalletTransaction.status == TransactionStatus.pending,
        WalletTransaction.payment_ref.like("wallet-%"),
        WalletTransaction.created_at >= now - PENDING_ORDER_TTL,
    ).count()


def reversals_of(db: Session, order_ids: Iterable[int]) -> dict[int, list[WalletTransaction]]:
    ids = list(order_ids)
    if not ids:
        return {}
    grouped: dict[int, list[WalletTransaction]] = {}
    for row in db.query(WalletTransaction).filter(
        WalletTransaction.transaction_type == TransactionType.reversal,
        WalletTransaction.related_tx_id.in_(ids),
    ).order_by(WalletTransaction.id).all():
        grouped.setdefault(row.related_tx_id, []).append(row)
    return grouped


def order_status(tx: WalletTransaction, reversals: list[WalletTransaction], now: Optional[datetime] = None) -> str:
    """pending | expired | failed | paid | partially_refunded | refunded | chargeback"""
    now = now or datetime.now(timezone.utc)
    if tx.status == TransactionStatus.failed:
        return "failed"
    if tx.status == TransactionStatus.pending:
        created = _aware(tx.created_at) if tx.created_at else now
        return "expired" if created < now - PENDING_ORDER_TTL else "pending"
    if any(r.action_type == CHARGEBACK for r in reversals):
        return "chargeback"
    if tx.reversed_credits and tx.reversed_credits >= tx.credits:
        return "refunded"
    if tx.reversed_credits:
        return "partially_refunded"
    return "paid"


def order_out(tx: WalletTransaction, reversals: list[WalletTransaction], packs: dict[int, CreditPackage]) -> dict:
    pack = packs.get(tx.package_id) if tx.package_id else None
    return {
        "reference": tx.payment_ref,
        "package": pack.name if pack else None,
        "package_code": pack.code if pack else None,
        "credits": tx.credits,
        "price": tx.egp_amount,
        "currency": "EGP",
        "status": order_status(tx, reversals),
        "credits_reversed": tx.reversed_credits or 0,
        "created_at": tx.created_at.isoformat() if tx.created_at else None,
        "paid_at": tx.settled_at.isoformat() if tx.settled_at else None,
    }


def orders_for_wallet(db: Session, wallet_id: int, limit: int = 50) -> list[dict]:
    rows = (
        db.query(WalletTransaction)
        .filter(WalletTransaction.wallet_id == wallet_id, WalletTransaction.transaction_type == TransactionType.topup,
                WalletTransaction.payment_ref.like("wallet-%"))
        .order_by(WalletTransaction.created_at.desc(), WalletTransaction.id.desc()).limit(limit).all()
    )
    reversals = reversals_of(db, [r.id for r in rows])
    pack_ids = {r.package_id for r in rows if r.package_id}
    packs = {p.id: p for p in db.query(CreditPackage).filter(CreditPackage.id.in_(pack_ids)).all()} if pack_ids else {}
    return [order_out(r, reversals.get(r.id, []), packs) for r in rows]


def order_by_reference(db: Session, wallet_id: int, reference: str) -> Optional[dict]:
    tx = db.query(WalletTransaction).filter(
        WalletTransaction.wallet_id == wallet_id, WalletTransaction.payment_ref == reference,
        WalletTransaction.transaction_type == TransactionType.topup,
    ).first()
    if tx is None:
        return None
    reversals = reversals_of(db, [tx.id]).get(tx.id, [])
    pack = db.query(CreditPackage).filter(CreditPackage.id == tx.package_id).first() if tx.package_id else None
    return order_out(tx, reversals, {pack.id: pack} if pack else {})


# ── Refunds and chargebacks ───────────────────────────────────────────────────

class ReversalRejected(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _minor(egp: Optional[float]) -> int:
    return round(float(egp or 0) * 100)


def reverse_purchase(
    db: Session, order: WalletTransaction, *, amount_minor: int, event_id: str, kind: str = REFUND,
    note: Optional[str] = None,
) -> dict:
    """Take back the credits an order bought, for `amount_minor` piasters refunded (or
    charged back). `order` must be a confirmed top-up the caller has locked. Commits.

    Idempotent on `event_id` (the provider's refund id, or an admin's idempotency key):
    a replay finds its reversal row and does nothing. The wallet row is locked, and the
    credits taken back are capped at what is still in the purchased bucket, so a
    learner who has already spent them is never driven below zero - the part that could
    not be recovered is recorded on the reversal row and in the security log for staff.
    Raises ReversalRejected for an order that was never paid or an amount that does not fit."""
    if order.transaction_type != TransactionType.topup or order.status != TransactionStatus.confirmed:
        raise ReversalRejected("order_not_paid")
    already = db.query(WalletTransaction).filter(
        WalletTransaction.transaction_type == TransactionType.reversal,
        WalletTransaction.provider_transaction_id == event_id,
    ).first()
    if already is not None:
        return {"status": "already_processed", "credits_reversed": order.reversed_credits or 0}

    total_minor = _minor(order.egp_amount)
    reversed_minor = sum(
        _minor(r.egp_amount) for r in db.query(WalletTransaction).filter(
            WalletTransaction.transaction_type == TransactionType.reversal,
            WalletTransaction.related_tx_id == order.id,
        )
    )
    remaining_minor = total_minor - reversed_minor
    if amount_minor <= 0 or amount_minor > remaining_minor:
        raise ReversalRejected("amount_mismatch")

    # The last piece takes whatever is left, so rounding never strands a credit.
    if amount_minor == remaining_minor:
        credits_due = order.credits - (order.reversed_credits or 0)
    else:
        credits_due = min(order.credits - (order.reversed_credits or 0), order.credits * amount_minor // total_minor)

    wallet = db.query(UserWallet).filter(UserWallet.id == order.wallet_id).with_for_update().one()
    recoverable = max(0, min(credits_due, wallet.purchased_credits or 0, wallet.credit_balance or 0))
    wallet.credit_balance = (wallet.credit_balance or 0) - recoverable
    wallet.purchased_credits = (wallet.purchased_credits or 0) - recoverable
    order.reversed_credits = (order.reversed_credits or 0) + credits_due
    shortfall = credits_due - recoverable

    label = "Chargeback" if kind == CHARGEBACK else "Refund"
    db.add(WalletTransaction(
        wallet_id=wallet.id, transaction_type=TransactionType.reversal, status=TransactionStatus.confirmed,
        credits=-recoverable, egp_amount=amount_minor / 100, payment_method=order.payment_method,
        provider_transaction_id=event_id, related_tx_id=order.id, package_id=order.package_id,
        description=(f"{label} of {credits_due} purchased credits" + (f" ({shortfall} already spent)" if shortfall else "")
                     + (f" - {note}" if note else ""))[:250],
        action_type=kind, balance_after=wallet.credit_balance, purchased_delta=-recoverable,
        settled_at=datetime.now(timezone.utc),
    ))
    try:
        db.commit()
    except IntegrityError:
        # uq_wallet_transactions_provider_txn: this provider event was just applied by another worker.
        db.rollback()
        return {"status": "already_processed", "credits_reversed": order.reversed_credits or 0}
    security_log.payment_event(
        kind=f"wallet_{kind}" + ("_shortfall" if shortfall else ""), ref=str(order.payment_ref),
        success=True, user_id=wallet.user_id,
    )
    if shortfall:
        logger.warning("wallet.reversal.unrecovered", extra={"order": order.payment_ref, "shortfall": shortfall})
    return {"status": "processed", "credits_reversed": order.reversed_credits, "recovered": recoverable,
            "unrecovered": shortfall}


def recorded_reversal_total(db: Session, order_id: int) -> int:
    return int(db.query(func.coalesce(func.sum(WalletTransaction.credits), 0)).filter(
        WalletTransaction.transaction_type == TransactionType.reversal,
        WalletTransaction.related_tx_id == order_id,
    ).scalar() or 0)
