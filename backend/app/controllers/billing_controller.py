"""Course checkout, purchase history, pricing administration and grants."""
import logging
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.authz import require_admin
from app.core.limiter import limiter
from app.core.legal import REFUND_POLICY_VERSION
from app.core.security import get_current_user, get_optional_user
from app.db.session import get_db
from app.models.billing import (
    BillingOrder, BillingPlan, CourseEnrollment, CourseOffer,
    SubscriptionOrder, UserSubscription,
)
from app.models.learning_path import Course
from app.models.user import User
from app.services.wallet import credit_purchases
from app.services.billing.access_service import active_enrollment
from app.services.billing import pro_ai_allowance as pro_ai
from app.services.billing.course_billing import current_offer
from app.services.billing.refunds import (
    RefundError, refund_eligibility, request_refund, transition_refund,
)
from app.services.learning.catalog_service import load_catalog_bundle
from app.services.payments.checkout import (
    PROVIDER as CHECKOUT_PROVIDER, language_of, require_payments_open, start_checkout,
)
from app.services.billing.subscriptions import (
    cancel_at_period_end, current_plan_code, current_subscription, plan_amount,
    release_stale_checkouts, start_free_trial, subscription_is_entitled,
)

logger = logging.getLogger("app.billing")
router = APIRouter()


def _refund_policy() -> dict:
    return {
        "version": REFUND_POLICY_VERSION,
        "trial_days": 7,
        "request_window_days": 7,
        "review_required": True,
        "original_payment_method_when_supported": True,
        "provider_processing_time_applies": True,
        "cancellation_is_not_refund": True,
        "subscription_credits_granted": 0,
    }


def _subscription_out(subscription: UserSubscription | None) -> dict | None:
    if subscription is None:
        return None
    return {
        "id": subscription.id,
        "plan": subscription.plan.code,
        "status": subscription.status,
        "billing_period": subscription.billing_period,
        "payment_provider": subscription.payment_provider,
        "current_period_start": subscription.current_period_start,
        "current_period_end": subscription.current_period_end,
        "cancel_at_period_end": subscription.cancel_at_period_end,
        "has_pro_access": subscription_is_entitled(subscription),
    }


def _subscription_order_out(order: SubscriptionOrder, *, admin: bool = False, timeline: bool = False) -> dict:
    eligible, reason = refund_eligibility(order)
    result = {
        "reference_number": order.reference_number,
        "plan": order.plan.code,
        "billing_period": order.billing_period,
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
        "created_at": order.created_at,
        "paid_at": order.paid_at,
        "refund_eligible": eligible,
        "refund_ineligibility_reason": reason,
        "refund": {
            "status": order.refund_status,
            "requested_at": order.refund_requested_at,
            "processed_at": order.refund_processed_at,
            "amount": order.refund_amount,
            "reason": order.refund_reason,
            "provider_reference": order.refund_provider_reference,
        },
        "refund_policy": _refund_policy(),
    }
    if admin:
        result.update({
            "id": order.id,
            "user_id": order.user_id,
            "customer": {"email": order.user.email, "name": order.user.full_name},
            "provider": order.provider,
            "provider_order_id": order.provider_order_id,
            "provider_transaction_id": order.provider_transaction_id,
            "merchant_order_id": order.merchant_order_id,
            "refund_admin_note": order.refund_admin_note,
        })
    if timeline:
        payment_events = [
            {
                "type": "payment",
                "status": "pending" if event.pending else ("succeeded" if event.success else "failed"),
                "provider_event_id": event.provider_event_id,
                "amount": event.amount,
                "currency": event.currency,
                "response_code": event.response_code,
                "created_at": event.created_at,
            }
            for event in order.events
        ]
        refund_events = [
            {
                "type": "refund",
                "from_status": event.from_status,
                "status": event.to_status,
                "provider_reference": event.provider_reference,
                "note": event.note if admin else None,
                "created_at": event.created_at,
            }
            for event in order.refund_events
        ]
        result["timeline"] = sorted(
            [*payment_events, *refund_events], key=lambda event: event["created_at"]
        )
    return result


def _raise_refund_error(exc: RefundError) -> None:
    raise _error(exc.status_code, exc.code, exc.message)


@router.get("/billing/catalog")
def billing_catalog(
    user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """The only public price list. Amounts returned here are major EGP units."""
    plans = db.query(BillingPlan).filter(BillingPlan.is_active.is_(True)).order_by(BillingPlan.id).all()
    packages = credit_purchases.active_packs(db)
    trial_eligible = bool(user) and not db.query(UserSubscription.id).filter(
        UserSubscription.user_id == user.id,
    ).first()
    return {
        "currency": "EGP",
        "vat_rate": 0.14,
        "prices_include_vat": True,
        "current_plan": current_plan_code(db, user.id if user else None),
        "trial_eligible": trial_eligible,
        "plans": [
            {
                "id": p.code,
                "monthly": p.monthly_price_minor / 100,
                "yearly": p.yearly_price_minor / 100,
                "signup_credits": p.signup_credits,
                "features": p.features,
                "popular": p.code == "pro",
            }
            for p in plans
        ],
        "packs": [
            {
                "id": str(p.id), "code": p.code, "name": p.name, "credits": p.credits,
                "bonus": p.bonus_credits or 0, "price": p.egp_price, "popular": bool(p.is_popular),
            }
            for p in packages
        ],
        "offer": None,
        "refund_policy": _refund_policy(),
    }


class SubscriptionCheckoutIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan: Literal["pro"]
    billing_period: Literal["monthly", "yearly"]
    # Accepted from older clients and ignored: Kashier's hosted page offers card
    # and mobile wallet itself and collects the wallet number there.
    method: Literal["card", "wallet"] = "card"
    phone_number: Optional[str] = Field(None, min_length=6, max_length=20, pattern=r"^\+?[0-9]{6,19}$")


class SubscriptionTrialIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan: Literal["pro"]
    billing_period: Literal["monthly", "yearly"]


@router.post("/billing/subscriptions/trial", status_code=status.HTTP_201_CREATED)
def subscription_trial(
    payload: SubscriptionTrialIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = db.query(BillingPlan).filter(
        BillingPlan.code == payload.plan, BillingPlan.is_active.is_(True),
    ).first()
    if plan is None:
        raise _error(404, "PLAN_NOT_FOUND", "Plan not found.")
    try:
        subscription = start_free_trial(db, current_user.id, plan, payload.billing_period)
    except (ValueError, IntegrityError):
        db.rollback()
        raise _error(409, "TRIAL_ALREADY_USED", "The free trial has already been used on this account.")
    return _subscription_out(subscription)


@router.post("/billing/subscriptions/checkout", dependencies=[Depends(require_payments_open)])
@limiter.limit("10/minute")
def subscription_checkout(
    request: Request,
    payload: SubscriptionCheckoutIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = db.query(BillingPlan).filter(
        BillingPlan.code == payload.plan, BillingPlan.is_active.is_(True),
    ).first()
    if plan is None:
        raise _error(404, "PLAN_NOT_FOUND", "Plan not found.")
    existing = current_subscription(db, current_user.id)
    if existing and existing.status == "trialing" and subscription_is_entitled(existing):
        raise _error(409, "TRIAL_ACTIVE", "The first charge is available after the free trial ends.")
    release_stale_checkouts(db, SubscriptionOrder, current_user.id)
    pending = db.query(SubscriptionOrder).filter(
        SubscriptionOrder.user_id == current_user.id,
        SubscriptionOrder.status == "pending",
    ).first()
    if pending:
        raise _error(409, "SUBSCRIPTION_CHECKOUT_PENDING", "A subscription checkout is already pending.", order_id=pending.id)

    amount = plan_amount(plan, payload.billing_period)
    merchant_order_id = f"subscription-{current_user.id}-{uuid.uuid4().hex}"
    order = SubscriptionOrder(
        user_id=current_user.id, plan_id=plan.id, billing_period=payload.billing_period,
        amount=amount, currency=plan.currency, provider=CHECKOUT_PROVIDER,
        merchant_order_id=merchant_order_id, status="pending",
    )
    db.add(order)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        pending = db.query(SubscriptionOrder).filter(
            SubscriptionOrder.user_id == current_user.id,
            SubscriptionOrder.status == "pending",
        ).first()
        if pending:
            raise _error(409, "SUBSCRIPTION_CHECKOUT_PENDING", "A subscription checkout is already pending.", order_id=pending.id)
        raise
    db.refresh(order)

    try:
        provider = start_checkout(
            kind="subscription", amount_minor=order.amount, currency=order.currency,
            merchant_order_id=order.merchant_order_id, user=current_user,
            description=f"Masar Pro ({order.billing_period})", language=language_of(request),
        )
    except HTTPException:
        order.status = "failed"
        db.commit()
        raise
    except Exception:
        db.rollback()
        order.status = "failed"
        db.commit()
        logger.exception("billing.subscription.provider_error", extra={"order_id": order.id})
        raise HTTPException(status_code=502, detail="The payment provider returned an unexpected response.")

    order.provider_order_id = provider["provider_order_id"]
    db.commit()
    return {
        "order_id": order.id, "reference_number": order.reference_number,
        "payment_url": provider["checkout_url"],
        "amount": order.amount, "currency": order.currency,
    }


@router.get("/billing/subscription")
def my_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest_order = (
        db.query(SubscriptionOrder).options(joinedload(SubscriptionOrder.plan))
        .filter(SubscriptionOrder.user_id == current_user.id)
        .order_by(SubscriptionOrder.created_at.desc()).first()
    )
    return {
        "plan": current_plan_code(db, current_user.id),
        "subscription": _subscription_out(current_subscription(db, current_user.id)),
        "latest_order": _subscription_order_out(latest_order) if latest_order else None,
        "refund_policy": _refund_policy(),
    }


@router.get("/billing/ai-allowance")
def my_ai_allowance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """The account's plan, its included AI allowance (paid Pro only; `null` on Free and
    during the trial, whose AI actions are paid from the wallet) and whether every
    course is open. Every value comes from server-side subscription and usage records."""
    subscription = pro_ai.eligible_subscription(db, current_user.id)
    plan = current_plan_code(db, current_user.id)
    current = current_subscription(db, current_user.id)
    return {
        "plan": plan,
        "ai_allowance": pro_ai.allowance_status(db, current_user.id).as_dict() if subscription else None,
        "all_courses_access": plan == "pro",
        # Where this account's AI actions are paid from right now. A trial opens every
        # course but pays for AI from the wallet until the first payment.
        "ai_billing": "allowance" if subscription else "wallet",
        "trial": bool(current and current.status == "trialing" and subscription_is_entitled(current)),
    }


@router.get("/billing/subscription-orders")
def my_subscription_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = (
        db.query(SubscriptionOrder).options(joinedload(SubscriptionOrder.plan))
        .filter(SubscriptionOrder.user_id == current_user.id)
        .order_by(SubscriptionOrder.created_at.desc()).all()
    )
    return [_subscription_order_out(order) for order in orders]


@router.get("/billing/subscription-orders/by-reference/{reference_number}")
def my_subscription_order_by_reference(
    reference_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(SubscriptionOrder).options(
        joinedload(SubscriptionOrder.plan), joinedload(SubscriptionOrder.refund_events),
    ).filter(
        SubscriptionOrder.reference_number == reference_number.upper(),
        SubscriptionOrder.user_id == current_user.id,
    ).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _subscription_order_out(order, timeline=True)


@router.get("/billing/subscription-orders/{order_id}")
def my_subscription_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(SubscriptionOrder).filter(
        SubscriptionOrder.id == order_id, SubscriptionOrder.user_id == current_user.id,
    ).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _subscription_order_out(order, timeline=True)


class RefundRequestIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reason: str = Field(..., min_length=5, max_length=2000)
    amount: Optional[int] = Field(None, gt=0)
    confirmed: bool
    idempotency_key: str = Field(..., min_length=16, max_length=64)  # stored with an actor prefix in a String(100)


@router.post("/billing/subscription-orders/{reference_number}/refund", status_code=status.HTTP_201_CREATED)
def create_refund_request(
    reference_number: str,
    payload: RefundRequestIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(SubscriptionOrder).filter(
        SubscriptionOrder.reference_number == reference_number.upper(),
        SubscriptionOrder.user_id == current_user.id,
    ).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        order = request_refund(
            db, order_id=order.id, user_id=current_user.id,
            amount=payload.amount or order.amount, reason=payload.reason,
            confirmed=payload.confirmed,
            # Client keys share a table with server keys ("provider-refund:...");
            # namespacing them means a learner can never pre-claim one.
            idempotency_key=f"user-{current_user.id}:{payload.idempotency_key}",
        )
    except RefundError as exc:
        _raise_refund_error(exc)
    return _subscription_order_out(order, timeline=True)


@router.post("/billing/subscription/cancel")
def cancel_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        subscription = cancel_at_period_end(db, current_user.id)
    except LookupError:
        raise HTTPException(status_code=404, detail="No active subscription")
    return _subscription_out(subscription)


def _error(status_code: int, code: str, message: str, **extra) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message, **extra})


def _course_by_public_id(db: Session, value: str | int) -> Optional[Course]:
    text = str(value)
    query = db.query(Course).filter(Course.is_active.is_(True))
    return query.filter(Course.id == int(text)).first() if text.isdigit() else query.filter(Course.slug == text).first()


def _offer_out(offer: CourseOffer) -> dict:
    return {
        "id": offer.id,
        "course_id": offer.course_id,
        "price_amount": offer.price_amount,
        "currency": offer.currency,
        "original_price_amount": offer.original_price_amount,
        "is_active": offer.is_active,
        "starts_at": offer.starts_at,
        "ends_at": offer.ends_at,
        "created_at": offer.created_at,
        "updated_at": offer.updated_at,
    }


def _order_out(order: BillingOrder) -> dict:
    course = order.course
    source = course.tool_course if course and course.tool_course else course.track_level if course else None
    return {
        "id": order.id,
        "course": {
            "id": course.id,
            "slug": course.slug,
            "title": course.title or (source.title if source else course.slug),
            "title_ar": course.title_ar or (source.title_ar if source else None),
        },
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
        "created_at": order.created_at,
        "paid_at": order.paid_at,
    }


class CheckoutIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_id: str | int
    # Accepted and ignored, as for subscriptions: Kashier's page picks the method.
    method: Literal["card", "wallet"] = "card"
    phone_number: Optional[str] = Field(None, min_length=6, max_length=20, pattern=r"^\+?[0-9]{6,19}$")


@router.post("/billing/checkout", dependencies=[Depends(require_payments_open)])
@limiter.limit("10/minute")
def checkout(
    request: Request,
    payload: CheckoutIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = _course_by_public_id(db, payload.course_id)
    if not course:
        raise _error(404, "COURSE_NOT_FOUND", "Course not found.")
    bundle = load_catalog_bundle(db)
    info = bundle.catalog.courses.get(course.id)
    if not info or not info.is_available:
        raise _error(409, "COURSE_UNAVAILABLE", "This course is not currently available.")
    if course.is_free:
        raise _error(409, "COURSE_IS_FREE", "This course does not require payment.")
    if active_enrollment(db, current_user.id, course.id, entitled_only=True):
        raise _error(409, "COURSE_ALREADY_OWNED", "You already own this course.", course_id=course.slug)

    release_stale_checkouts(db, BillingOrder, current_user.id, course_id=course.id)
    pending_order = db.query(BillingOrder.id).filter(
        BillingOrder.user_id == current_user.id,
        BillingOrder.course_id == course.id,
        BillingOrder.status == "pending",
    ).first()
    if pending_order:
        raise _error(
            409, "COURSE_CHECKOUT_PENDING", "A checkout for this course is already pending.",
            order_id=pending_order.id,
        )

    offer = current_offer(db, course.id, lock=True)
    if not offer:
        raise _error(409, "COURSE_OFFER_UNAVAILABLE", "No active price is available for this course.")

    merchant_order_id = f"course-{course.id}-{uuid.uuid4().hex}"
    order = BillingOrder(
        user_id=current_user.id,
        purchasable_type="course",
        purchasable_id=course.id,
        course_id=course.id,
        offer_id=offer.id,
        amount=offer.price_amount,
        currency=offer.currency,
        provider=CHECKOUT_PROVIDER,
        merchant_order_id=merchant_order_id,
        status="pending",
    )
    db.add(order)
    try:
        db.commit()
    except IntegrityError:
        # The partial unique index resolves check/insert races across workers.
        db.rollback()
        pending_order = db.query(BillingOrder.id).filter(
            BillingOrder.user_id == current_user.id,
            BillingOrder.course_id == course.id,
            BillingOrder.status == "pending",
        ).first()
        if pending_order:
            raise _error(
                409, "COURSE_CHECKOUT_PENDING", "A checkout for this course is already pending.",
                order_id=pending_order.id,
            )
        raise
    db.refresh(order)

    try:
        provider = start_checkout(
            kind="course_payment", amount_minor=order.amount, currency=order.currency,
            merchant_order_id=order.merchant_order_id, user=current_user,
            description=f"Masar course: {course.slug}", language=language_of(request),
        )
    except HTTPException:
        order.status = "failed"
        db.commit()
        raise
    except Exception:
        # Anything else (an unexpected provider response) must not leave a
        # pending order behind to block the next attempt.
        db.rollback()
        order.status = "failed"
        db.commit()
        logger.exception("billing.checkout.provider_error", extra={"order_id": order.id})
        raise HTTPException(status_code=502, detail="The payment provider returned an unexpected response.")

    order.provider_order_id = provider["provider_order_id"]
    db.commit()
    logger.info(
        "billing.checkout.created",
        extra={"order_id": order.id, "user_id": current_user.id, "course_id": course.id},
    )
    return {
        "order_id": order.id,
        "payment_url": provider["checkout_url"],
        "amount": order.amount,
        "currency": order.currency,
    }


@router.get("/billing/courses/{course_id}/offer")
def get_course_offer(course_id: str, db: Session = Depends(get_db)):
    course = _course_by_public_id(db, course_id)
    if not course:
        raise _error(404, "COURSE_NOT_FOUND", "Course not found.")
    offer = current_offer(db, course.id)
    if not offer:
        raise _error(404, "COURSE_OFFER_UNAVAILABLE", "No active price is available for this course.")
    return {"course_id": course.slug, **{k: v for k, v in _offer_out(offer).items() if k in (
        "price_amount", "currency", "original_price_amount",
    )}}


@router.get("/billing/orders")
def my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = (
        db.query(BillingOrder)
        .options(joinedload(BillingOrder.course).joinedload(Course.tool_course),
                 joinedload(BillingOrder.course).joinedload(Course.track_level))
        .filter(BillingOrder.user_id == current_user.id)
        .order_by(BillingOrder.created_at.desc())
        .all()
    )
    return [_order_out(order) for order in orders]


@router.get("/billing/orders/{order_id}")
def my_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = (
        db.query(BillingOrder)
        .options(joinedload(BillingOrder.course).joinedload(Course.tool_course),
                 joinedload(BillingOrder.course).joinedload(Course.track_level))
        .filter(BillingOrder.id == order_id, BillingOrder.user_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_out(order)


class OfferCreate(BaseModel):
    course_id: str | int
    price_amount: int = Field(..., gt=0)
    currency: Literal["EGP"] = "EGP"
    original_price_amount: Optional[int] = Field(None, ge=0)
    is_active: bool = True
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    @model_validator(mode="after")
    def valid_window_and_price(self):
        if self.original_price_amount is not None and self.original_price_amount < self.price_amount:
            raise ValueError("original_price_amount must be at least price_amount")
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        return self


class OfferPatch(BaseModel):
    price_amount: Optional[int] = Field(None, gt=0)
    original_price_amount: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


@router.get("/admin/course-offers")
def admin_offers(
    course_id: Optional[int] = Query(None, gt=0),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(CourseOffer).order_by(CourseOffer.created_at.desc())
    if course_id is not None:
        query = query.filter(CourseOffer.course_id == course_id)
    return [_offer_out(offer) for offer in query.all()]


@router.post("/admin/course-offers", status_code=status.HTTP_201_CREATED)
def create_offer(
    payload: OfferCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    course = _course_by_public_id(db, payload.course_id)
    if not course:
        raise _error(404, "COURSE_NOT_FOUND", "Course not found.")
    if payload.is_active and db.query(CourseOffer.id).filter(
        CourseOffer.course_id == course.id, CourseOffer.is_active.is_(True),
    ).first():
        raise _error(409, "ACTIVE_OFFER_EXISTS", "Deactivate the current offer first.")
    offer = CourseOffer(course_id=course.id, **payload.model_dump(exclude={"course_id"}))
    db.add(offer)
    if offer.is_active:
        course.is_free = False
    db.commit()
    db.refresh(offer)
    return _offer_out(offer)


@router.patch("/admin/course-offers/{offer_id}")
def update_offer(
    offer_id: int,
    payload: OfferPatch,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    offer = db.query(CourseOffer).filter(CourseOffer.id == offer_id).with_for_update().first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("is_active") is True and db.query(CourseOffer.id).filter(
        CourseOffer.course_id == offer.course_id,
        CourseOffer.is_active.is_(True),
        CourseOffer.id != offer.id,
    ).first():
        raise _error(409, "ACTIVE_OFFER_EXISTS", "Deactivate the current offer first.")
    for key, value in changes.items():
        setattr(offer, key, value)
    if offer.original_price_amount is not None and offer.original_price_amount < offer.price_amount:
        raise _error(422, "INVALID_ORIGINAL_PRICE", "original_price_amount must be at least price_amount.")
    if offer.starts_at and offer.ends_at and offer.ends_at <= offer.starts_at:
        raise _error(422, "INVALID_OFFER_WINDOW", "ends_at must be after starts_at.")
    if offer.is_active:
        offer.course.is_free = False
    db.commit()
    db.refresh(offer)
    return _offer_out(offer)


@router.get("/admin/orders")
def admin_orders(
    order_status: Optional[str] = Query(None, alias="status"),
    course_id: Optional[int] = Query(None, gt=0),
    user_id: Optional[int] = Query(None, gt=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(BillingOrder).options(
        joinedload(BillingOrder.course).joinedload(Course.tool_course),
        joinedload(BillingOrder.course).joinedload(Course.track_level),
    ).order_by(BillingOrder.created_at.desc())
    if order_status:
        query = query.filter(BillingOrder.status == order_status)
    if course_id:
        query = query.filter(BillingOrder.course_id == course_id)
    if user_id:
        query = query.filter(BillingOrder.user_id == user_id)
    return [_order_out(order) for order in query.limit(limit).all()]


@router.get("/admin/orders/{order_id}")
def admin_order(order_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    order = db.query(BillingOrder).options(
        joinedload(BillingOrder.course).joinedload(Course.tool_course),
        joinedload(BillingOrder.course).joinedload(Course.track_level),
    ).filter(BillingOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_out(order)


@router.get("/admin/subscriptions")
def admin_subscriptions(
    subscription_status: Optional[str] = Query(None, alias="status"),
    billing_period: Optional[Literal["monthly", "yearly"]] = None,
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(UserSubscription).options(
        joinedload(UserSubscription.plan), joinedload(UserSubscription.user),
    ).order_by(UserSubscription.current_period_end.desc())
    if subscription_status:
        query = query.filter(UserSubscription.status == subscription_status)
    if billing_period:
        query = query.filter(UserSubscription.billing_period == billing_period)
    return [
        {
            **_subscription_out(subscription),
            "user_id": subscription.user_id,
            "email": subscription.user.email,
        }
        for subscription in query.limit(limit).all()
    ]


@router.get("/admin/subscription-orders")
def admin_subscription_orders(
    reference_number: Optional[str] = None,
    provider_transaction_id: Optional[str] = None,
    customer: Optional[str] = None,
    order_id: Optional[int] = Query(None, gt=0),
    refund_status: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(SubscriptionOrder).options(
        joinedload(SubscriptionOrder.plan), joinedload(SubscriptionOrder.user),
    ).order_by(SubscriptionOrder.created_at.desc())
    if reference_number:
        query = query.filter(SubscriptionOrder.reference_number == reference_number.upper())
    if provider_transaction_id:
        query = query.filter(SubscriptionOrder.provider_transaction_id == provider_transaction_id)
    if customer:
        query = query.join(User, User.id == SubscriptionOrder.user_id).filter(
            (User.email.ilike(f"%{customer}%")) | (User.full_name.ilike(f"%{customer}%"))
        )
    if order_id:
        query = query.filter(SubscriptionOrder.id == order_id)
    if refund_status:
        query = query.filter(SubscriptionOrder.refund_status == refund_status)
    return [_subscription_order_out(order, admin=True) for order in query.limit(limit).all()]


@router.get("/admin/subscription-orders/{reference_number}")
def admin_subscription_order(
    reference_number: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(SubscriptionOrder).options(
        joinedload(SubscriptionOrder.plan), joinedload(SubscriptionOrder.user),
        joinedload(SubscriptionOrder.events), joinedload(SubscriptionOrder.refund_events),
    ).filter(SubscriptionOrder.reference_number == reference_number.upper()).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _subscription_order_out(order, admin=True, timeline=True)


class AdminRefundTransitionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["under_review", "approved", "rejected", "processing", "refunded", "failed"]
    idempotency_key: str = Field(..., min_length=16, max_length=64)  # stored with an actor prefix in a String(100)
    amount: Optional[int] = Field(None, gt=0)
    provider_reference: Optional[str] = Field(None, max_length=100)
    note: Optional[str] = Field(None, max_length=4000)


@router.post("/admin/subscription-orders/{reference_number}/refund-transition")
def admin_refund_transition(
    reference_number: str,
    payload: AdminRefundTransitionIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(SubscriptionOrder).filter(
        SubscriptionOrder.reference_number == reference_number.upper(),
    ).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        order = transition_refund(
            db, order_id=order.id, to_status=payload.status,
            actor_user_id=current_user.id, idempotency_key=f"admin-{current_user.id}:{payload.idempotency_key}",
            note=payload.note, provider_reference=payload.provider_reference,
            refund_amount=payload.amount,
        )
    except RefundError as exc:
        _raise_refund_error(exc)
    return _subscription_order_out(order, admin=True, timeline=True)


class AdminEnrollmentIn(BaseModel):
    user_id: int = Field(..., gt=0)
    course_id: str | int
    source: Literal["admin_grant"] = "admin_grant"


@router.post("/admin/enrollments", status_code=status.HTTP_201_CREATED)
def admin_enroll(
    payload: AdminEnrollmentIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if not db.query(User.id).filter(User.id == payload.user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    course = _course_by_public_id(db, payload.course_id)
    if not course:
        raise _error(404, "COURSE_NOT_FOUND", "Course not found.")
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == payload.user_id,
        CourseEnrollment.course_id == course.id,
    ).with_for_update().first()
    if enrollment:
        # A support grant is idempotent and must never rewrite the audit
        # trail of access that was already purchased.
        if enrollment.source != "purchase":
            enrollment.status = "active"
            enrollment.source = "admin_grant"
            enrollment.expires_at = None
    else:
        enrollment = CourseEnrollment(
            user_id=payload.user_id, course_id=course.id,
            source="admin_grant", status="active", expires_at=None,
        )
        db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    logger.info(
        "billing.enrollment.admin_granted",
        extra={"user_id": payload.user_id, "course_id": course.id, "admin_id": current_user.id},
    )
    return {
        "id": enrollment.id,
        "user_id": enrollment.user_id,
        "course_id": course.slug,
        "source": enrollment.source,
        "status": enrollment.status,
        "enrolled_at": enrollment.enrolled_at,
        "expires_at": enrollment.expires_at,
    }
