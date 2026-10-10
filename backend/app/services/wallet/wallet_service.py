"""
backend/app/services/wallet/wallet_service.py

Central service for all credit operations.
Import deduct_credits() in any controller that calls an LLM.
"""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings

from app.core.authz import email_verification_error
from app.core.metrics import record_credit_denial, record_credits_spent
from app.models.user import User, UserRole
from app.models.billing import BillingOrder, CourseEnrollment
from app.models.wallet import UserWallet, WalletTransaction, TransactionType, TransactionStatus, PaymentMethod
from app.services.billing import pro_ai_allowance as pro_ai


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
    # Mentor v2 (POST /mentor/message): the same price as a chat message. Rule-based replies —
    # a quiz question taken from the course, a proactive prompt — are never charged at all.
    "mentor_message":    2,
}

FREE_PLAN_CREDITS = 40
FREE_PLAN_MIGRATION_MARKER = "free_plan_40_migration_v1"


def migrate_free_wallets_to_40(db: Session) -> int:
    """Idempotent one-time normalizer used by migration verification/tools.
    Same rule as migration 021: raise eligible free wallets to at least 40,
    never reduce one.

    Paid credit buyers and users with purchased/admin-granted course access
    are deliberately excluded. History is appended; no old row is rewritten.
    """
    migrated = 0
    users = db.query(User).filter(User.role == UserRole.student).all()
    for user in users:
        wallet = get_or_create_wallet(user.id, db)
        already_done = db.query(WalletTransaction.id).filter(
            WalletTransaction.wallet_id == wallet.id,
            WalletTransaction.action_type == FREE_PLAN_MIGRATION_MARKER,
        ).first()
        bought_credits = db.query(WalletTransaction.id).filter(
            WalletTransaction.wallet_id == wallet.id,
            WalletTransaction.transaction_type == TransactionType.topup,
            WalletTransaction.status == TransactionStatus.confirmed,
        ).first()
        paid_course = db.query(CourseEnrollment.id).filter(
            CourseEnrollment.user_id == user.id,
            CourseEnrollment.source.in_(("purchase", "admin_grant")),
        ).first()
        paid_order = db.query(BillingOrder.id).filter(
            BillingOrder.user_id == user.id, BillingOrder.status == "paid",
        ).first()
        if already_done or bought_credits or paid_course or paid_order:
            continue

        wallet = db.query(UserWallet).filter(UserWallet.id == wallet.id).with_for_update().one()
        # A floor, never a reset: a balance at or above 40 is left alone.
        if (wallet.credit_balance or 0) >= FREE_PLAN_CREDITS:
            continue
        delta = FREE_PLAN_CREDITS - (wallet.credit_balance or 0)
        wallet.credit_balance = FREE_PLAN_CREDITS
        wallet.promo_credits_remaining = 0
        wallet.promo_expires_at = None
        db.add(WalletTransaction(
            wallet_id=wallet.id, transaction_type=TransactionType.bonus,
            status=TransactionStatus.confirmed, credits=delta,
            payment_method=PaymentMethod.admin,
            description="Free plan balance raised to 40 credits",
            action_type=FREE_PLAN_MIGRATION_MARKER,
            balance_after=FREE_PLAN_CREDITS,
        ))
        db.commit()
        migrated += 1
    return migrated


def get_or_create_wallet(user_id: int, db: Session) -> UserWallet:
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    if not wallet:
        wallet = UserWallet(user_id=user_id, credit_balance=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


def expire_promo_credits_if_due(wallet: UserWallet, db: Session, commit: bool = True) -> int:
    """Withdraw any UNSPENT promo credits once the user's window closes.

    Lazy rather than scheduled: it runs whenever the wallet is touched, so
    there is no cron to forget and no window where an expired balance is
    still spendable. Returns how many credits were removed.

    Only ever removes promo credits the user did not spend — purchased
    credits are untouched — and never takes the balance below the Free
    plan's 40 credits (release decision 2026-10-08): a launch-promo wallet
    ends where a new signup starts, not at zero. A balance already under 40
    loses nothing.

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

    balance = wallet.credit_balance or 0
    # Never reaches into purchased credits: only the rest of the balance can lapse.
    removed = min(
        wallet.promo_credits_remaining,
        max(0, balance - FREE_PLAN_CREDITS),
        max(0, balance - (wallet.purchased_credits or 0)),
    )
    wallet.credit_balance = balance - removed
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


def _require_verified_email(user_id: int, db: Session) -> None:
    """Refuse to spend credits for an account that has not confirmed its
    email address.

    This lives here, rather than as a dependency on each billable route,
    because deduct_credits() is the one function every credit spend in the
    app already passes through. A guard here cannot be forgotten when the
    next billable endpoint is added, and it is structurally guaranteed to
    run BEFORE the balance is touched and before the caller reaches its
    provider call (every billable controller deducts first, then invokes
    the LLM, then refunds on failure).

    Reads the User row rather than trusting anything on the request: the
    caller passes a bare user_id, and verification status must reflect the
    database now, not whenever a token was minted.
    """
    verified = db.query(User.is_verified).filter(User.id == user_id).scalar()
    # `None` means no such user — that is not this function's error to
    # report, so leave it to the existing flow rather than masking a
    # missing account as an unverified one.
    if verified is None:
        return
    if not verified:
        raise email_verification_error()


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

    # Before anything is read or written on the wallet: an unverified
    # account may not spend. Raising here guarantees no balance change and
    # no provider call, so a rejected request costs the user nothing and
    # costs us nothing.
    _require_verified_email(user_id, db)

    # A Pro subscriber's AI actions are paid from the plan's included allowance
    # first. Past it, the wallet's PURCHASED credits (and only those - signup and
    # promo credits stay out of reach) pay for the action, within their own daily
    # safety limit; with none to spend the request is refused instead.
    if action_type in pro_ai.PRO_AI_ACTIONS:
        subscription = pro_ai.eligible_subscription(db, user_id)
        if subscription is not None:
            return _charge_pro_allowance(user_id, action_type, cost, subscription, db)

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

    # A retried request (same Idempotency-Key) that was already charged and not
    # refunded is not charged again.
    request_key = pro_ai.current_request_key(action_type)
    if request_key and _already_charged(db, wallet.id, request_key):
        db.rollback()
        raise _duplicate_request(action_type)

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

    return _debit_wallet(wallet, cost, action_type, db, description=description, request_key=request_key)


def _duplicate_request(action_type: str) -> HTTPException:
    return HTTPException(
        status_code=409,
        detail={"error": "duplicate_request", "action": action_type,
                "message": "This request was already received; it is not run or charged twice."},
    )


def _already_charged(db: Session, wallet_id: int, request_key: str) -> bool:
    """Whether a deduction under this request key is still standing (not refunded).
    Called with the wallet row locked, so two retries cannot both pass."""
    ids = [row.id for row in db.query(WalletTransaction.id).filter(
        WalletTransaction.wallet_id == wallet_id,
        WalletTransaction.transaction_type == TransactionType.deduction,
        WalletTransaction.request_key == request_key,
    ).all()]
    if not ids:
        return False
    refunded = {row.related_tx_id for row in db.query(WalletTransaction.related_tx_id).filter(
        WalletTransaction.wallet_id == wallet_id,
        WalletTransaction.transaction_type == TransactionType.refund,
        WalletTransaction.related_tx_id.in_(ids),
    ).all()}
    return any(i not in refunded for i in ids)


def _debit_wallet(
    wallet: UserWallet, cost: int, action_type: str, db: Session, *,
    description: str = None, purchased_only: bool = False, request_key: str = None,
) -> dict:
    """Take `cost` from a wallet row the caller has locked and already checked, and
    write the ledger row. Commits.

    Where the credits come from: the part of the balance that was not bought
    (signup and promo credits, promo first) is spent first, purchased credits last,
    so expiry can never take away credits the user actually paid for.
    `purchased_only` is for a Pro subscriber past the included allowance, who may
    spend purchased credits and nothing else."""
    record_credits_spent(action_type, cost)
    purchased = min(wallet.purchased_credits or 0, wallet.credit_balance or 0)
    included_part = 0 if purchased_only else max(0, (wallet.credit_balance or 0) - purchased)
    from_purchased = cost if purchased_only else max(0, cost - included_part)

    wallet.credit_balance  -= cost
    wallet.lifetime_spent  += cost
    wallet.purchased_credits = purchased - from_purchased
    from_included = cost - from_purchased
    if from_included and wallet.promo_credits_remaining > 0:
        wallet.promo_credits_remaining = max(0, wallet.promo_credits_remaining - from_included)

    tx = WalletTransaction(
        wallet_id        = wallet.id,
        transaction_type = TransactionType.deduction,
        status           = TransactionStatus.confirmed,
        credits          = -cost,
        description      = description or f"Used {action_type.replace('_', ' ').title()}",
        action_type      = action_type,
        balance_after    = wallet.credit_balance,
        purchased_delta  = -from_purchased,
        request_key      = request_key,
    )
    db.add(tx)
    db.commit()

    return {"credits_used": cost, "balance_after": wallet.credit_balance,
            "purchased_credits_used": from_purchased}


def purchased_spent_since(db: Session, wallet_id: int, since: datetime) -> int:
    """Net purchased credits spent since `since`: what deductions took from the
    purchased bucket, less what refunds put back."""
    spent = db.query(func.coalesce(func.sum(WalletTransaction.purchased_delta), 0)).filter(
        WalletTransaction.wallet_id == wallet_id,
        WalletTransaction.transaction_type.in_((TransactionType.deduction, TransactionType.refund)),
        WalletTransaction.created_at >= since,
    ).scalar()
    return -int(spent or 0)


PRO_LIMIT_MESSAGE = (
    "You've used your {limit} included AI credits for the current 4-hour window. Your course access "
    "remains available. More AI credits will become available as earlier usage leaves the window."
)


def _charge_purchased_after_allowance(user_id: int, action_type: str, cost: int, db: Session):
    """A Pro subscriber past the included allowance: pay from PURCHASED credits when
    there are enough and the rolling-24-hour purchased-credit limit allows it.
    Returns the charge result, or None when there is nothing to spend (the caller
    then refuses with the allowance's own 429). Signup and promo credits are never
    used here, and the unverified-email check has already passed."""
    get_or_create_wallet(user_id, db)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).with_for_update().one()
    expire_promo_credits_if_due(wallet, db, commit=False)

    request_key = pro_ai.current_request_key(action_type)
    if request_key and _already_charged(db, wallet.id, request_key):
        db.rollback()
        raise _duplicate_request(action_type)

    purchased = min(wallet.purchased_credits or 0, wallet.credit_balance or 0)
    if purchased < cost:
        db.rollback()
        return None

    limit = settings.PURCHASED_CREDITS_DAILY_LIMIT
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    if purchased_spent_since(db, wallet.id, since) + cost > limit:
        db.rollback()
        record_credit_denial(action_type)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "purchased_credits_daily_limit",
                "message": f"For safety, purchased credits can be used up to {limit} per 24 hours "
                           "once your included AI credits are used up. Please try again later.",
                "action": action_type,
                "credits_needed": cost,
                "daily_limit": limit,
            },
            headers={"Retry-After": "3600"},
        )
    result = _debit_wallet(
        wallet, cost, action_type, db, purchased_only=True, request_key=request_key,
        description=f"Used {action_type.replace('_', ' ').title()} (purchased credits)",
    )
    return {**result, "source": "purchased_credits"}


def _charge_pro_allowance(user_id: int, action_type: str, cost: int, subscription, db: Session) -> dict:
    """Reserve `cost` from the Pro allowance (see pro_ai_allowance); past it, pay from
    purchased credits if there are any; otherwise refuse with 429. Signup and promo
    credits are never used for a Pro subscriber's AI actions."""
    try:
        usage = pro_ai.reserve(
            db, user_id, subscription, action_type, cost, request_key=pro_ai.current_request_key(action_type),
        )
    except pro_ai.AllowanceExceeded as exc:
        paid = _charge_purchased_after_allowance(user_id, action_type, cost, db)
        if paid is not None:
            return paid
        record_credit_denial(action_type)
        status = exc.status
        retry_at = exc.available_at
        headers = {}
        if retry_at is not None:
            wait = max(1, int((retry_at - datetime.now(timezone.utc)).total_seconds()) + 1)
            headers["Retry-After"] = str(wait)
        message = PRO_LIMIT_MESSAGE.format(limit=status.limit) if status.remaining == 0 else (
            f"This action needs {cost} AI credits and {status.remaining} of your {status.limit} included "
            "credits are left in the current 4-hour window. Your course access remains available."
        )
        raise HTTPException(
            status_code=429,
            detail={
                "error": "pro_ai_limit_reached",
                "message": message,
                "action": action_type,
                "credits_needed": cost,
                **status.as_dict(),
                "retry_at": pro_ai._iso(retry_at),
            },
            headers=headers or None,
        )
    except pro_ai.DuplicateRequest:
        raise _duplicate_request(action_type)
    pro_ai.remember(pro_ai.RequestCharge(user_id, action_type, cost, usage.id))
    remaining = pro_ai.allowance_status(db, user_id).remaining
    wallet = get_or_create_wallet(user_id, db)
    return {"credits_used": cost, "source": "pro_allowance", "allowance_remaining": remaining,
            "balance_after": wallet.credit_balance}


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

    # This request paid from the Pro allowance: give those credits back to the
    # allowance, not to the wallet (which was never charged).
    charge, already_released = pro_ai.take(user_id, action_type, cost)
    if charge is not None:
        pro_ai.release(db, charge.usage_id, reason=reason)
    if charge is not None or already_released:
        return get_or_create_wallet(user_id, db)

    get_or_create_wallet(user_id, db)
    wallet = (
        db.query(UserWallet)
        .filter(UserWallet.user_id == user_id)
        .with_for_update()
        .one()
    )

    # The deduction this refund answers: the latest one for this action and price that
    # has not been refunded yet. It says how much of the charge came out of purchased
    # credits, which go back to the purchased bucket (they never expire); the rest
    # lands in the ordinary balance, as before. With no such deduction (a refund
    # issued outside the request that charged) everything lands in the ordinary balance.
    refunded_ids = db.query(WalletTransaction.related_tx_id).filter(
        WalletTransaction.wallet_id == wallet.id,
        WalletTransaction.transaction_type == TransactionType.refund,
        WalletTransaction.related_tx_id.isnot(None),
    )
    original = (
        db.query(WalletTransaction)
        .filter(
            WalletTransaction.wallet_id == wallet.id,
            WalletTransaction.transaction_type == TransactionType.deduction,
            WalletTransaction.action_type == action_type,
            WalletTransaction.credits == -cost,
            ~WalletTransaction.id.in_(refunded_ids),
        )
        .order_by(WalletTransaction.id.desc())
        .first()
    )
    back_to_purchased = min(cost, -(original.purchased_delta or 0)) if original is not None else 0

    wallet.credit_balance += cost
    wallet.purchased_credits = (wallet.purchased_credits or 0) + back_to_purchased
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
        purchased_delta  = back_to_purchased,
        related_tx_id    = original.id if original is not None else None,
    )
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet


def confirm_pending_topup(tx: WalletTransaction, db: Session, *, commit: bool = True) -> UserWallet:
    """Release the credits recorded on an already-pending top-up row.

    This is the second half of the top-up state machine. `add_credits(...,
    status="pending")` writes the row without touching the balance; this
    moves it to confirmed and pays the credits out. It is NOT the same
    operation as add_credits and cannot be expressed with it — add_credits
    would insert a *second* transaction row, double-counting the purchase
    in the wallet history.

    It exists because both confirmation paths — the Paymob webhook and the
    admin/manual confirmation — had this logic pasted inline, and a credit
    payout duplicated in two places is a payout that can drift in one of
    them. Now there is exactly one.

    Locking: takes SELECT ... FOR UPDATE on the wallet row itself rather
    than trusting the caller to have done it. Both callers already lock the
    transaction row before getting here, which is what serialises two
    concurrent confirmations of the SAME payment; this lock is what
    serialises a confirmation against an unrelated concurrent spend on the
    same wallet, so that neither read-modify-write loses the other.

    Idempotent by design: a row that is not pending is left exactly as it
    is and no credits are paid out. Paymob retries webhooks, and a retry
    that arrives after the first one committed must not top the user up
    twice. The caller's own `status == pending` filter is the fast path;
    this is the one that holds under a race.
    """
    if tx.status != TransactionStatus.pending:
        return db.query(UserWallet).filter(UserWallet.id == tx.wallet_id).one()

    wallet = db.query(UserWallet).filter(UserWallet.id == tx.wallet_id).with_for_update().one()
    wallet.credit_balance     += tx.credits
    wallet.lifetime_purchased += tx.credits
    # Bought credits sit in their own bucket: they never expire and plan changes leave them alone.
    wallet.purchased_credits   = (wallet.purchased_credits or 0) + tx.credits
    tx.status = TransactionStatus.confirmed
    tx.balance_after = wallet.credit_balance
    tx.purchased_delta = tx.credits
    tx.settled_at = datetime.now(timezone.utc)

    if commit:
        db.commit()
    else:
        db.flush()
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
        wallet.credit_balance += credits
        # Welcome/admin bonuses are not purchases. Keeping this counter
        # purchase-only lets migrations identify paying users accurately.
        if transaction_type == "topup":
            wallet.lifetime_purchased += credits
            wallet.purchased_credits = (wallet.purchased_credits or 0) + credits

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
        purchased_delta  = credits if (status == "confirmed" and transaction_type == "topup") else 0,
        settled_at       = datetime.now(timezone.utc) if (status == "confirmed" and transaction_type == "topup") else None,
    )
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet
