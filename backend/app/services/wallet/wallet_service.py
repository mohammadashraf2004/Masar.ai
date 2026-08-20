"""
backend/app/services/wallet/wallet_service.py

Central service for all credit operations.
Import deduct_credits() in any controller that calls an LLM.
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.wallet import UserWallet, WalletTransaction, TransactionType, TransactionStatus, PaymentMethod


# ── Credit costs per action ───────────────────────────────────────────────────
CREDIT_COSTS = {
    "mentor_chat":       2,
    "code_review":       5,
    "skill_gap":         8,
    "mock_interview":    3,
    "exam_grading":     10,
    "roadmap":           5,
}


def get_or_create_wallet(user_id: int, db: Session) -> UserWallet:
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    if not wallet:
        wallet = UserWallet(user_id=user_id, credit_balance=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


def deduct_credits(user_id: int, action_type: str, db: Session) -> dict:
    """
    Deduct credits for an AI action.
    Raises HTTP 402 if insufficient balance.
    Returns dict with credits_used and balance_after.

    Locks the wallet row for the duration of the transaction (SELECT ... FOR
    UPDATE) so two concurrent requests from the same user can't both read the
    same balance, both pass the sufficient-funds check, and both deduct —
    a double-spend race that existed here before.
    """
    cost = CREDIT_COSTS.get(action_type, 1)

    # Cheap, rare path: make sure a wallet row exists at all.
    get_or_create_wallet(user_id, db)

    wallet = (
        db.query(UserWallet)
        .filter(UserWallet.user_id == user_id)
        .with_for_update()
        .one()
    )

    if wallet.credit_balance < cost:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "insufficient_credits",
                "message": f"You need {cost} credits for this action but only have {wallet.credit_balance}.",
                "credits_needed": cost,
                "credits_available": wallet.credit_balance,
                "action": action_type,
            }
        )

    wallet.credit_balance  -= cost
    wallet.lifetime_spent  += cost

    tx = WalletTransaction(
        wallet_id        = wallet.id,
        transaction_type = TransactionType.deduction,
        status           = TransactionStatus.confirmed,
        credits          = -cost,
        description      = f"Used {action_type.replace('_', ' ').title()}",
        action_type      = action_type,
        balance_after    = wallet.credit_balance,
    )
    db.add(tx)
    db.commit()

    return {"credits_used": cost, "balance_after": wallet.credit_balance}


def add_credits(
    user_id: int,
    credits: int,
    db: Session,
    egp_amount: float = None,
    payment_method: str = "admin",
    payment_ref: str = None,
    description: str = "Credit top-up",
    status: str = "confirmed",
    transaction_type: str = "topup",
) -> UserWallet:
    """Add credits to a wallet (top-up or bonus)."""
    wallet = get_or_create_wallet(user_id, db)

    if status == "confirmed":
        wallet.credit_balance     += credits
        wallet.lifetime_purchased += credits

    tx = WalletTransaction(
        wallet_id        = wallet.id,
        transaction_type = TransactionType(transaction_type),
        status           = TransactionStatus(status),
        credits          = credits,
        egp_amount       = egp_amount,
        payment_method   = PaymentMethod(payment_method) if payment_method else None,
        payment_ref      = payment_ref,
        description      = description,
        balance_after    = wallet.credit_balance,
    )
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet