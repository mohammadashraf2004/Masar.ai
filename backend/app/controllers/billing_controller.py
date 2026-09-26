"""Course checkout, purchase history, pricing administration and grants."""
import logging
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.authz import require_admin
from app.core.limiter import limiter
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.billing import BillingOrder, CourseEnrollment, CourseOffer
from app.models.learning_path import Course
from app.models.user import User
from app.services.billing.access_service import active_enrollment
from app.services.billing.course_billing import current_offer
from app.services.learning.catalog_service import load_catalog_bundle
from app.services.payments import paymob_service

logger = logging.getLogger("app.billing")
router = APIRouter()


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
    method: Literal["card", "wallet"] = "card"
    phone_number: Optional[str] = Field(None, min_length=6, max_length=20, pattern=r"^\+?[0-9]{6,19}$")

    @model_validator(mode="after")
    def wallet_phone(self):
        if self.method == "wallet" and not self.phone_number:
            raise ValueError("phone_number is required for method=wallet")
        return self


@router.post("/billing/checkout")
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
        provider="paymob",
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
        provider = paymob_service.init_payment_minor(
            amount_minor=order.amount,
            currency=order.currency,
            merchant_order_id=order.merchant_order_id,
            method=payload.method,
            full_name=current_user.full_name,
            email=current_user.email,
            phone_number=payload.phone_number or "01000000000",
        )
    except paymob_service.PaymobConfigError as exc:
        order.status = "failed"
        db.commit()
        raise HTTPException(status_code=503, detail=str(exc))
    except httpx.HTTPStatusError as exc:
        order.status = "failed"
        db.commit()
        logger.warning("Paymob rejected course checkout", extra={"order_id": order.id, "status": exc.response.status_code})
        raise HTTPException(status_code=502, detail="The payment provider rejected this request.")
    except httpx.HTTPError:
        order.status = "failed"
        db.commit()
        raise HTTPException(status_code=502, detail="Could not reach Paymob. Please try again.")

    order.provider_order_id = str(provider["paymob_order_id"])
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
