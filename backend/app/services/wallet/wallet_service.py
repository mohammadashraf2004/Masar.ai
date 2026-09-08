"""
backend/app/services/wallet/wallet_service.py

Central service for all credit operations.
Import deduct_credits() in any controller that calls an LLM.
"""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.metrics import record_credit_denial, record_credits_spent
from app.models.wallet import UserWallet, WalletTransaction, TransactionType, TransactionStatus, PaymentMethod


# ── Credit costs per action ───────────────────────────────────────────────────
CREDIT_COSTS = {
    "mentor_chat":       2,
    "code_review":       5,
    "skill_gap":         8,
    "mock_interview":    3,
    "exam_grading":     10,
    "roadmap":           5,
    "exercise_feedback": 2,
    # A hint is the cheapest thing the tutor does — one short answer. Listed
    # explicitly rather than relying on the get(..., 1) default so the price
    # is discoverable through GET /wallet/costs like every other action.
    "project_hint":      1,
    # Same price, same reasoning, for the challenge tutor. Challenge
    # *enrolment* is not here: its price lives on the ChallengeProject row
    # (`credit_cost`) and varies per challenge, so it is passed to
    # deduct_credits() as an explicit `cost` instead.
    "challenge_hint":    1,
}


def get_or_create_wallet(user_id: int, db: Session) -> UserWallet:
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    if not wallet:
        wallet = UserWallet(user_id=user_id, credit_balance=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


def grant_launch_promo(user_id: int, db: Session) -> int:
    """Grant the launch-promo credit bundle to a brand-new account.

    Returns the number of credits granted (0 when the promo is closed, so
    the caller falls back to the ordinary starter grant).

    Called exactly once, from registration. Both the eligibility check and
    the expiry date come from the server clock and server config — there
    is no request field that influences either.
    """
    if not settings.promo_is_open() or settings.LAUNCH_PROMO_CREDITS <= 0:
        return 0

    credits = settings.LAUNCH_PROMO_CREDITS
    wallet = add_credits(
        user_id, credits, db,
        payment_method="admin",
        description=f"Launch promo — {credits} free credits",
        transaction_type="bonus",
    )

    wallet.promo_credits_remaining = credits
    if settings.LAUNCH_PROMO_DAYS > 0:
        wallet.promo_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.LAUNCH_PROMO_DAYS)
    db.commit()
    return credits


def expire_promo_credits_if_due(wallet: UserWallet, db: Session, commit: bool = True) -> int:
    """Withdraw any UNSPENT promo credits once the user's window closes.

    Lazy rather than scheduled: it runs whenever the wallet is touched, so
    there is no cron to forget and no window where an expired balance is
    still spendable. Returns how many credits were removed.

    Only ever removes promo credits the user did not spend — purchased
    credits are untouched, and the balance is floored at zero.

    `commit=False` is for callers that are already inside a transaction
    holding SELECT ... FOR UPDATE on this wallet row — deduct_credits is
    the one that matters. Committing there would end that transaction and
    release the row lock *before* the balance check and the decrement,
    which is precisely the double-spend the lock exists to prevent: two
    concurrent spends against an expiring wallet could both get past the
    check. Those callers flush instead, so the expiry is visible to the
    rest of their own transaction and lands atomically with the spend.
    """
    expires_at = wallet.promo_expires_at
    if not expires_at or wallet.promo_credits_remaining <= 0:
        return 0
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) < expires_at:
        return 0

    removed = min(wallet.promo_credits_remaining, wallet.credit_balance)
    wallet.credit_balance = max(0, wallet.credit_balance - removed)
    wallet.promo_credits_remaining = 0
    wallet.promo_expires_at = None

    if removed:
        db.add(WalletTransaction(
            wallet_id=wallet.id,
            transaction_type=TransactionType.expiry,
            status=TransactionStatus.confirmed,
            credits=-removed,
            description="Launch promo credits expired",
            action_type="promo_expiry",
            balance_after=wallet.credit_balance,
        ))
    if commit:
        db.commit()
    else:
        db.flush()
    return removed


def deduct_credits(
    user_id: int,
    action_type: str,
    db: Session,
    cost: int = None,
    description: str = None,
) -> dict:
    """
    Deduct credits for an AI action.
    Raises HTTP 402 if insufficient balance.
    Returns dict with credits_used and balance_after.

    Locks the wallet row for the duration of the transaction (SELECT ... FOR
    UPDATE) so two concurrent requests from the same user can't both read the
    same balance, both pass the sufficient-funds check, and both deduct —
    a double-spend race that existed here before.

    `cost` overrides the CREDIT_COSTS lookup, for the one kind of spend
    whose price is not a per-action constant: challenge enrolment, which
    charges whatever `ChallengeProject.credit_cost` says. It exists so that
    path can go through this function instead of adjusting the wallet
    inline — an inline deduction skips the row lock, the promo-expiry
    check, the promo-balance decrement and the spend metric, which is how
    challenge spending used to leave `promo_credits_remaining` overstated
    and let already-expired promo credits be spent.

    `description` overrides the generated transaction description, so a
    challenge deduction can still read "Enrolled in challenge: X" in the
    wallet history rather than a generic "Used Challenge Enroll".
    """
    if cost is None:
        cost = CREDIT_COSTS.get(action_type, 1)

    # Cheap, rare path: make sure a wallet row exists at all.
    get_or_create_wallet(user_id, db)

    wallet = (
        db.query(UserWallet)
        .filter(UserWallet.user_id == user_id)
        .with_for_update()
        .one()
    )

    # Inside the row lock, before the sufficient-funds check: an expired
    # promo balance must not be spendable, and checking first would let a
    # concurrent request slip through on credits that are already gone.
    # commit=False: committing here would release the row lock taken above
    # before the check and decrement below. See that function's docstring.
    expire_promo_credits_if_due(wallet, db, commit=False)

    if wallet.credit_balance < cost:
        # Worth a metric of its own: a rising denial rate is the difference
        # between "nobody is using the AI features" and "everybody is, and
        # they've run out" — the two look identical in request counts.
        record_credit_denial(action_type)
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

    record_credits_spent(action_type, cost)
    wallet.credit_balance  -= cost
    wallet.lifetime_spent  += cost
    # Spend promo credits before purchased ones, so expiry can never take
    # away credits the user actually paid for.
    if wallet.promo_credits_remaining > 0:
        wallet.promo_credits_remaining = max(0, wallet.promo_credits_remaining - cost)

    tx = WalletTransaction(
        wallet_id        = wallet.id,
        transaction_type = TransactionType.deduction,
        status           = TransactionStatus.confirmed,
        credits          = -cost,
        description      = description or f"Used {action_type.replace('_', ' ').title()}",
        action_type      = action_type,
        balance_after    = wallet.credit_balance,
    )
    db.add(tx)
    db.commit()

    return {"credits_used": cost, "balance_after": wallet.credit_balance}


def refund_credits(
    user_id: int,
    action_type: str,
    db: Session,
    reason: str,
    cost: int = None,
) -> UserWallet:
    """Give back credits for an AI action that was charged but never delivered.

    Exists because `add_credits` is the wrong tool for this: it increments
    `lifetime_purchased`, so refunding through it would report a failed
    request as credits the user had *bought*, inflating a number the wallet
    UI shows them.

    This is the exact inverse of deduct_credits, and mirrors it deliberately:
    same CREDIT_COSTS lookup, same SELECT ... FOR UPDATE on the wallet row
    (so a refund can't interleave with a concurrent spend and lose an
    update), and it commits before returning — a refund that stays in an
    uncommitted session is the same as no refund at all.

    Deliberately NOT restored: promo credits. deduct_credits spends promo
    balance first, but promo credits expire on a date, and handing back a
    promo credit whose window has since closed would be either worthless or
    a quiet extension of the promotion. The refund lands in the ordinary
    spendable balance instead, which slightly favours the user — the right
    direction to err when we failed to deliver what they paid for.

    `cost` mirrors the override on deduct_credits, and exists for the same
    single reason: challenge enrolment prices itself from the challenge
    row. A refund must hand back exactly what was taken, so if the
    deduction passed a cost, the refund reversing it has to pass the same
    one.
    """
    if cost is None:
        cost = CREDIT_COSTS.get(action_type, 1)

    get_or_create_wallet(user_id, db)
    wallet = (
        db.query(UserWallet)
        .filter(UserWallet.user_id == user_id)
        .with_for_update()
        .one()
    )

    wallet.credit_balance += cost
    # The spend is being undone, so it should stop counting as spent. Floored
    # at zero: a refund must never drive lifetime_spent negative, whatever
    # state the row was already in.
    wallet.lifetime_spent = max(0, (wallet.lifetime_spent or 0) - cost)

    tx = WalletTransaction(
        wallet_id        = wallet.id,
        transaction_type = TransactionType.refund,
        status           = TransactionStatus.confirmed,
        credits          = cost,          # positive: credits coming back
        description      = reason,
        action_type      = action_type,   # same label as the deduction it reverses
        balance_after    = wallet.credit_balance,
    )
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet


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