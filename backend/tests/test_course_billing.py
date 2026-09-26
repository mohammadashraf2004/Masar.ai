"""Course purchase lifecycle: server pricing, Paymob settlement and access."""
import hashlib
import hmac as hmac_lib

import pytest

from app.models.billing import BillingOrder, CourseEnrollment, CourseOffer, PaymentTransaction
from app.models.learning_path import Course
from app.services.learning.catalog_service import load_catalog_bundle
from app.services.payments import paymob_service
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import make_admin, register


SECRET = "course-webhook-secret"


def _paid_available_course(db):
    bundle = load_catalog_bundle(db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)
    course.is_free = False
    offer = CourseOffer(course_id=course.id, price_amount=149900, currency="EGP", is_active=True)
    db.add(offer)
    db.commit()
    db.refresh(course)
    db.refresh(offer)
    return course, offer


def _checkout(client, db, monkeypatch, who):
    course, offer = _paid_available_course(db)
    captured = {}

    def fake_init(**kwargs):
        captured.update(kwargs)
        return {"checkout_url": "https://accept.paymob.test/checkout", "paymob_order_id": 777001}

    monkeypatch.setattr(paymob_service, "init_payment_minor", fake_init)
    response = client.post(
        "/api/v1/billing/checkout",
        headers=who["headers"],
        json={"course_id": course.slug},
    )
    assert response.status_code == 200, response.text
    order = db.query(BillingOrder).filter(BillingOrder.id == response.json()["order_id"]).one()
    return course, offer, order, captured


def _webhook_obj(order, *, transaction_id=99101, amount=None, success=True, pending=False):
    return {
        "amount_cents": order.amount if amount is None else amount,
        "created_at": "2026-09-26T12:00:00.000000",
        "currency": order.currency,
        "error_occured": False,
        "has_parent_transaction": False,
        "id": transaction_id,
        "integration_id": 123,
        "is_3d_secure": True,
        "is_auth": False,
        "is_capture": False,
        "is_refunded": False,
        "is_standalone_payment": True,
        "is_voided": False,
        "order": {"id": int(order.provider_order_id), "merchant_order_id": order.merchant_order_id},
        "owner": 42,
        "pending": pending,
        "source_data": {"pan": "1234", "sub_type": "MasterCard", "type": "card"},
        "success": success,
    }


def _sign(obj):
    concatenated = "".join(
        paymob_service._stringify(paymob_service._extract(obj, field))
        for field in paymob_service._HMAC_FIELDS
    )
    return hmac_lib.new(SECRET.encode(), concatenated.encode(), hashlib.sha512).hexdigest()


def _post_webhook(client, obj):
    return client.post(
        f"/api/v1/payments/paymob/webhook?hmac={_sign(obj)}",
        json={"type": "TRANSACTION", "obj": obj},
    )


def test_checkout_uses_database_minor_units_and_provider_id(learn_client, learn_db, learn_catalog, monkeypatch):
    who = register(learn_client)
    course, offer, order, captured = _checkout(learn_client, learn_db, monkeypatch, who)
    assert captured["amount_minor"] == 149900
    assert captured["currency"] == "EGP"
    assert order.amount == offer.price_amount == 149900
    assert order.provider_order_id == "777001"
    assert order.course_id == course.id


def test_checkout_rejects_missing_offer(learn_client, learn_db, learn_catalog):
    who = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)
    course.is_free = False
    learn_db.commit()
    response = learn_client.post(
        "/api/v1/billing/checkout",
        headers=who["headers"],
        json={"course_id": course.slug},
    )
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "COURSE_OFFER_UNAVAILABLE"


def test_checkout_rejects_a_client_supplied_amount(learn_client, learn_db, learn_catalog):
    who = register(learn_client)
    course, _ = _paid_available_course(learn_db)
    response = learn_client.post(
        "/api/v1/billing/checkout",
        headers=who["headers"],
        json={"course_id": course.slug, "amount": 1},
    )
    assert response.status_code == 422


def test_checkout_requires_auth_and_an_active_course(learn_client, learn_db, learn_catalog):
    assert learn_client.post(
        "/api/v1/billing/checkout", json={"course_id": "does-not-exist"},
    ).status_code == 401

    who = register(learn_client)
    missing = learn_client.post(
        "/api/v1/billing/checkout", headers=who["headers"], json={"course_id": "does-not-exist"},
    )
    assert missing.status_code == 404

    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)
    course.is_active = False
    learn_db.commit()
    inactive = learn_client.post(
        "/api/v1/billing/checkout", headers=who["headers"], json={"course_id": course.slug},
    )
    assert inactive.status_code == 404


def test_free_course_access_does_not_require_an_enrollment(learn_client, learn_db, learn_catalog):
    who = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)

    response = learn_client.get(
        f"/api/v1/learning/courses/{course.slug}/access", headers=who["headers"],
    )
    assert response.status_code == 200
    assert response.json() == {"has_access": True, "reason": "free", "enrollment_id": None}


def test_paid_content_is_redacted_but_preview_remains_readable(
    learn_client, learn_db, learn_catalog,
):
    who = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(
        c for c in bundle.courses.values()
        if c.tool_course_id and bundle.catalog.courses[c.id].is_available
    )
    course.is_free = False
    tool_course = course.tool_course
    topic = tool_course.topics[0]
    lesson = topic.lessons[0]
    learn_db.commit()

    locked = learn_client.get(
        f"/api/v1/tool-courses/{tool_course.slug}", headers=who["headers"],
    )
    assert locked.status_code == 200
    locked_lesson = locked.json()["topics"][0]["lessons"][0]
    assert locked_lesson["content"] == ""
    assert locked_lesson["is_locked"] is True
    assert locked_lesson["course_slug"] == course.slug

    progress = learn_client.post(
        f"/api/v1/tool-courses/topics/{topic.id}/progress",
        headers=who["headers"], json={"lesson_id": lesson.id},
    )
    assert progress.status_code == 403
    assert progress.json()["detail"]["code"] == "COURSE_PURCHASE_REQUIRED"

    lesson.is_preview = True
    learn_db.commit()
    preview = learn_client.get(
        f"/api/v1/tool-courses/{tool_course.slug}", headers=who["headers"],
    )
    preview_lesson = preview.json()["topics"][0]["lessons"][0]
    assert preview_lesson["content"] == "c"
    assert preview_lesson["is_preview"] is True
    assert preview_lesson["is_locked"] is False


def test_successful_webhook_creates_one_paid_order_transaction_and_enrollment(
    learn_client, learn_db, learn_catalog, monkeypatch,
):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, who)
    obj = _webhook_obj(order)

    first = _post_webhook(learn_client, obj)
    second = _post_webhook(learn_client, obj)
    assert first.status_code == second.status_code == 200
    assert second.json()["status"] == "already_processed"

    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "paid"
    assert learn_db.query(PaymentTransaction).filter_by(order_id=order.id).count() == 1
    enrollment = learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).one()
    assert enrollment.source == "purchase" and enrollment.expires_at is None

    access = learn_client.get(f"/api/v1/learning/courses/{course.slug}/access", headers=who["headers"])
    assert access.json()["has_access"] is True
    assert access.json()["reason"] == "purchase"


def test_wrong_amount_is_recorded_but_never_grants_access(learn_client, learn_db, learn_catalog, monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, who)
    response = _post_webhook(learn_client, _webhook_obj(order, amount=1))
    assert response.status_code == 200
    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "failed"
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 0
    tx = learn_db.query(PaymentTransaction).filter_by(order_id=order.id).one()
    assert tx.response_code == "amount_mismatch"


def test_failed_payment_does_not_enroll(learn_client, learn_db, learn_catalog, monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, who)
    assert _post_webhook(learn_client, _webhook_obj(order, success=False)).status_code == 200
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 0


def test_pending_then_final_webhook_with_same_transaction_enrolls_once(
    learn_client, learn_db, learn_catalog, monkeypatch,
):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, who)

    pending = _post_webhook(
        learn_client, _webhook_obj(order, transaction_id=77123, success=False, pending=True),
    )
    assert pending.status_code == 200
    assert pending.json()["success"] is False
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 0

    final = _post_webhook(
        learn_client, _webhook_obj(order, transaction_id=77123, success=True, pending=False),
    )
    assert final.status_code == 200
    assert final.json()["success"] is True
    assert learn_db.query(PaymentTransaction).filter_by(order_id=order.id).count() == 1
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 1


def test_invalid_hmac_changes_nothing(learn_client, learn_db, learn_catalog, monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    _, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, who)
    response = learn_client.post(
        "/api/v1/payments/paymob/webhook?hmac=wrong",
        json={"type": "TRANSACTION", "obj": _webhook_obj(order)},
    )
    assert response.status_code == 401
    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "pending"


def test_owned_course_cannot_be_purchased_twice(learn_client, learn_db, learn_catalog, monkeypatch):
    who = register(learn_client)
    course, _, _, _ = _checkout(learn_client, learn_db, monkeypatch, who)
    learn_db.add(CourseEnrollment(user_id=who["id"], course_id=course.id, source="admin_grant", status="active"))
    learn_db.commit()
    response = learn_client.post(
        "/api/v1/billing/checkout", headers=who["headers"], json={"course_id": course.slug},
    )
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "COURSE_ALREADY_OWNED"


def test_course_cannot_have_two_pending_checkouts(learn_client, learn_db, learn_catalog, monkeypatch):
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, who)
    response = learn_client.post(
        "/api/v1/billing/checkout", headers=who["headers"], json={"course_id": course.slug},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == {
        "code": "COURSE_CHECKOUT_PENDING",
        "message": "A checkout for this course is already pending.",
        "order_id": order.id,
    }


def test_admin_grant_unlocks_without_fake_transaction(learn_client, learn_db, learn_catalog):
    student = register(learn_client)
    admin = register(learn_client)
    make_admin(learn_db, admin["id"])
    course, _ = _paid_available_course(learn_db)

    denied = learn_client.post(
        "/api/v1/admin/enrollments", headers=student["headers"],
        json={"user_id": student["id"], "course_id": course.slug, "source": "admin_grant"},
    )
    assert denied.status_code == 403
    granted = learn_client.post(
        "/api/v1/admin/enrollments", headers=admin["headers"],
        json={"user_id": student["id"], "course_id": course.slug, "source": "admin_grant"},
    )
    assert granted.status_code == 201, granted.text
    assert learn_db.query(PaymentTransaction).count() == 0
    access = learn_client.get(f"/api/v1/learning/courses/{course.slug}/access", headers=student["headers"])
    assert access.json()["reason"] == "admin_grant"


def test_non_admin_cannot_manage_course_pricing(learn_client, learn_db, learn_catalog):
    student = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)
    response = learn_client.post(
        "/api/v1/admin/course-offers",
        headers=student["headers"],
        json={"course_id": course.slug, "price_amount": 149900, "currency": "EGP"},
    )
    assert response.status_code == 403


def test_admin_can_create_and_update_an_egp_offer(learn_client, learn_db, learn_catalog):
    admin = register(learn_client)
    make_admin(learn_db, admin["id"])
    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)

    created = learn_client.post(
        "/api/v1/admin/course-offers",
        headers=admin["headers"],
        json={"course_id": course.slug, "price_amount": 149900, "currency": "EGP"},
    )
    assert created.status_code == 201, created.text
    offer_id = created.json()["id"]
    assert created.json()["price_amount"] == 149900

    updated = learn_client.patch(
        f"/api/v1/admin/course-offers/{offer_id}",
        headers=admin["headers"],
        json={"price_amount": 129900, "original_price_amount": 149900},
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["price_amount"] == 129900
    assert updated.json()["original_price_amount"] == 149900
    learn_db.refresh(course)
    assert course.is_free is False


def test_user_cannot_read_another_users_order(learn_client, learn_db, learn_catalog, monkeypatch):
    owner = register(learn_client)
    stranger = register(learn_client)
    _, _, order, _ = _checkout(learn_client, learn_db, monkeypatch, owner)
    assert learn_client.get(f"/api/v1/billing/orders/{order.id}", headers=stranger["headers"]).status_code == 404
