"""Course purchase lifecycle: server pricing, Kashier settlement (Paymob for historical orders) and access."""
import hashlib
import hmac as hmac_lib

import pytest

from app.models.billing import BillingOrder, CourseEnrollment, CourseOffer, PaymentTransaction
from app.models.learning import Exercise, Lesson, Quiz
from app.models.learning_path import Course
from app.services.learning.catalog_service import load_catalog_bundle
from app.services.payments import paymob_service
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import accept_written_answers, make_admin, register
from tests.kashier_fixtures import kashier  # noqa: F401


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


def _checkout(client, db, kashier, who):
    course, offer = _paid_available_course(db)
    response = client.post(
        "/api/v1/billing/checkout",
        headers=who["headers"],
        json={"course_id": course.slug},
    )
    assert response.status_code == 200, response.text
    order = db.query(BillingOrder).filter(BillingOrder.id == response.json()["order_id"]).one()
    return course, offer, order, kashier.sessions[order.provider_order_id]


def _historical_paymob_order(db, who, course, offer, provider_order_id="777001"):
    """An order Paymob took before the switch to Kashier: its callbacks still reconcile."""
    order = BillingOrder(
        user_id=who["id"], purchasable_type="course", purchasable_id=course.id, course_id=course.id,
        offer_id=offer.id, amount=offer.price_amount, currency="EGP", provider="paymob",
        merchant_order_id=f"course-{course.id}-historical-{provider_order_id}",
        provider_order_id=provider_order_id, status="pending",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def _kashier_pay(kashier, client, order, *, amount="1499.00", status="SUCCESS", transaction_id=None, record="PAID"):
    kashier.record(order.provider_order_id, order.merchant_order_id, amount, status=record)
    return kashier.post(client, kashier.data(order.merchant_order_id, amount, status=status,
                                             transaction_id=transaction_id))


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


def test_checkout_uses_database_minor_units_and_provider_id(learn_client, learn_db, learn_catalog, kashier):
    who = register(learn_client)
    course, offer, order, captured = _checkout(learn_client, learn_db, kashier, who)
    assert captured["amount_minor"] == 149900
    assert captured["currency"] == "EGP"
    assert order.amount == offer.price_amount == 149900
    assert order.provider == "kashier"
    assert order.provider_order_id == kashier.session_of(order.merchant_order_id)
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


def test_free_course_access_is_the_two_lesson_preview_not_full_access(learn_client, learn_db, learn_catalog):
    """Since the Free/Pro migration, no course is free outright: a signed-in Free
    account gets the ordered two-lesson preview (access_service.free_lesson_ids)
    and nothing past it, regardless of the legacy `is_free` flag."""
    who = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if bundle.catalog.courses[c.id].is_available)

    response = learn_client.get(
        f"/api/v1/learning/courses/{course.slug}/access", headers=who["headers"],
    )
    assert response.status_code == 200
    assert response.json() == {
        "has_access": False, "reason": "purchase_required", "enrollment_id": None, "free_lesson_count": 2,
    }


def test_paid_content_is_redacted_but_the_first_two_ordered_lessons_remain_readable(
    learn_client, learn_db, learn_catalog,
):
    who = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(
        c for c in bundle.courses.values()
        if c.tool_course_id and bundle.catalog.courses[c.id].is_available
    )
    tool_course = course.tool_course
    topic = tool_course.topics[0]
    first_lesson = topic.lessons[0]
    first_lesson.source_key = "PREVIEW-TEST/L001"
    # The fixture course has one lesson; add two more so a third, paywalled
    # lesson exists past the two-lesson free preview.
    second_lesson = Lesson(
        tool_topic_id=topic.id, source_key="PREVIEW-TEST/L002",
        title="Free preview two", content="two", order=first_lesson.order + 1,
    )
    third_lesson = Lesson(
        tool_topic_id=topic.id, source_key="PREVIEW-TEST/L003",
        title="Locked lesson three", content="three", order=first_lesson.order + 2,
    )
    free_exercise = Exercise(
        tool_topic_id=topic.id, source_key="PREVIEW-TEST/L001/x1",
        title="Preview exercise", description="free exercise", starter_code=None,
    )
    locked_exercise = Exercise(
        tool_topic_id=topic.id, source_key="PREVIEW-TEST/L003/x1",
        title="Paid exercise", description="paid exercise", starter_code=None,
    )
    free_quiz = Quiz(
        tool_topic_id=topic.id, source_key="PREVIEW-TEST/L002/quiz", title="Preview quiz",
        questions=[{"question": "Free?", "options": ["Yes", "No"], "correct": 0}],
    )
    locked_quiz = Quiz(
        tool_topic_id=topic.id, source_key="PREVIEW-TEST/L003/quiz", title="Paid quiz",
        questions=[{"question": "Paid?", "options": ["Yes", "No"], "correct": 0}],
    )
    learn_db.add_all([
        second_lesson, third_lesson, free_exercise, locked_exercise, free_quiz, locked_quiz,
    ])
    learn_db.commit()

    locked = learn_client.get(
        f"/api/v1/tool-courses/{tool_course.slug}", headers=who["headers"],
    )
    assert locked.status_code == 200
    lessons_by_id = {lesson["id"]: lesson for t in locked.json()["topics"] for lesson in t["lessons"]}
    locked_lesson = lessons_by_id[third_lesson.id]
    assert locked_lesson["content"] == ""
    assert locked_lesson["is_locked"] is True
    assert locked_lesson["course_slug"] == course.slug

    progress = learn_client.post(
        f"/api/v1/tool-courses/topics/{topic.id}/progress",
        headers=who["headers"], json={"lesson_id": third_lesson.id},
    )
    assert progress.status_code == 403
    assert progress.json()["detail"]["code"] == "COURSE_PURCHASE_REQUIRED"

    preview_one, preview_two = lessons_by_id[first_lesson.id], lessons_by_id[second_lesson.id]
    for preview_lesson in (preview_one, preview_two):
        assert preview_lesson["content"]
        assert preview_lesson["is_preview"] is True
        assert preview_lesson["is_locked"] is False

    topic_body = next(t for t in locked.json()["topics"] if t["id"] == topic.id)
    exercises = {item["id"]: item for item in topic_body["exercises"]}
    quizzes = {item["id"]: item for item in topic_body["quizzes"]}
    assert exercises[free_exercise.id]["description"] == "free exercise"
    assert exercises[free_exercise.id]["is_locked"] is False
    assert exercises[locked_exercise.id]["description"] == ""
    assert exercises[locked_exercise.id]["is_locked"] is True
    assert quizzes[free_quiz.id]["questions"]
    assert quizzes[free_quiz.id]["is_locked"] is False
    assert quizzes[locked_quiz.id]["questions"] == []
    assert quizzes[locked_quiz.id]["is_locked"] is True

    # Readable is not completed: without an accepted answer nothing counts.
    unanswered = learn_client.post(
        f"/api/v1/tool-courses/topics/{topic.id}/progress",
        headers=who["headers"], json={"exercise_id": free_exercise.id},
    )
    assert unanswered.status_code == 409 and unanswered.json()["detail"]["code"] == "ANSWER_NOT_ACCEPTED_YET"
    accept_written_answers(learn_db, who["id"], [free_exercise.id])
    free_exercise_progress = learn_client.post(
        f"/api/v1/tool-courses/topics/{topic.id}/progress",
        headers=who["headers"], json={"exercise_id": free_exercise.id},
    )
    assert free_exercise_progress.status_code == 200
    locked_exercise_progress = learn_client.post(
        f"/api/v1/tool-courses/topics/{topic.id}/progress",
        headers=who["headers"], json={"exercise_id": locked_exercise.id},
    )
    assert locked_exercise_progress.status_code == 403

    assert learn_client.post(
        f"/api/v1/tracks/quizzes/{free_quiz.id}/submit",
        headers=who["headers"], json={"answers": {"0": 0}},
    ).status_code == 200
    assert learn_client.post(
        f"/api/v1/tracks/quizzes/{locked_quiz.id}/submit",
        headers=who["headers"], json={"answers": {"0": 0}},
    ).status_code == 403


def test_admin_has_full_course_content_without_subscription_or_purchase(
    learn_client, learn_db, learn_catalog,
):
    admin = register(learn_client)
    make_admin(learn_db, admin["id"])
    bundle = load_catalog_bundle(learn_db)
    course = next(
        c for c in bundle.courses.values()
        if c.tool_course_id and bundle.catalog.courses[c.id].is_available
    )

    access = learn_client.get(
        f"/api/v1/learning/courses/{course.slug}/access", headers=admin["headers"],
    )
    assert access.status_code == 200
    assert access.json()["has_access"] is True
    assert access.json()["reason"] == "admin"

    content = learn_client.get(
        f"/api/v1/tool-courses/{course.tool_course.slug}", headers=admin["headers"],
    )
    assert content.status_code == 200
    for topic in content.json()["topics"]:
        assert all(not item["is_locked"] for item in topic["lessons"])
        assert all(not item["is_locked"] for item in topic["exercises"])
        assert all(not item["is_locked"] for item in topic["quizzes"])
        assert all(not item["is_locked"] for item in topic["projects"])


def test_successful_webhook_creates_one_paid_order_transaction_and_enrollment(
    learn_client, learn_db, learn_catalog, kashier,
):
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, kashier, who)
    kashier.record(order.provider_order_id, order.merchant_order_id, "1499.00")
    data = kashier.data(order.merchant_order_id, "1499.00")

    first = kashier.post(learn_client, data)
    second = kashier.post(learn_client, data)
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


def test_wrong_amount_is_recorded_but_never_grants_access(learn_client, learn_db, learn_catalog, kashier):
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, kashier, who)
    response = _kashier_pay(kashier, learn_client, order, amount="0.01")
    assert response.status_code == 200
    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "failed"
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 0
    tx = learn_db.query(PaymentTransaction).filter_by(order_id=order.id).one()
    assert tx.response_code == "amount_mismatch"


def test_failed_payment_does_not_enroll(learn_client, learn_db, learn_catalog, kashier):
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, kashier, who)
    assert _kashier_pay(kashier, learn_client, order, status="FAILURE").status_code == 200
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 0


def test_pending_then_final_webhook_with_same_transaction_enrolls_once(
    learn_client, learn_db, learn_catalog, kashier,
):
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, kashier, who)

    pending = _kashier_pay(kashier, learn_client, order, status="PENDING", transaction_id="TX-77123")
    assert pending.status_code == 200
    assert pending.json()["success"] is False
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 0

    final = _kashier_pay(kashier, learn_client, order, status="SUCCESS", transaction_id="TX-77123")
    assert final.status_code == 200
    assert final.json()["success"] is True
    assert learn_db.query(PaymentTransaction).filter_by(order_id=order.id).count() == 1
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).count() == 1


def test_invalid_signature_changes_nothing(learn_client, learn_db, learn_catalog, kashier):
    who = register(learn_client)
    _, _, order, _ = _checkout(learn_client, learn_db, kashier, who)
    kashier.record(order.provider_order_id, order.merchant_order_id, "1499.00")
    response = kashier.post(learn_client, kashier.data(order.merchant_order_id, "1499.00"), signature="wrong")
    assert response.status_code == 401
    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "pending"


def test_a_historical_paymob_order_still_settles_through_paymob_only(
    learn_client, learn_db, learn_catalog, kashier, monkeypatch,
):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    course, offer = _paid_available_course(learn_db)
    order = _historical_paymob_order(learn_db, who, course, offer)

    # A Kashier-signed callback naming it is ignored: Kashier never took this order.
    ignored = kashier.post(learn_client, kashier.data(order.merchant_order_id, "1499.00"))
    assert ignored.json() == {"status": "no matching order"}

    obj = _webhook_obj(order)
    assert _post_webhook(learn_client, obj).json()["success"] is True
    assert _post_webhook(learn_client, obj).json()["status"] == "already_processed"
    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "paid"
    tx = learn_db.query(PaymentTransaction).filter_by(order_id=order.id).one()
    assert tx.provider == "paymob"
    assert learn_db.query(CourseEnrollment).filter_by(user_id=who["id"], course_id=course.id).one().source == "purchase"


def test_invalid_paymob_hmac_changes_nothing(learn_client, learn_db, learn_catalog, monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    who = register(learn_client)
    course, offer = _paid_available_course(learn_db)
    order = _historical_paymob_order(learn_db, who, course, offer, provider_order_id="777002")
    response = learn_client.post(
        "/api/v1/payments/paymob/webhook?hmac=wrong",
        json={"type": "TRANSACTION", "obj": _webhook_obj(order)},
    )
    assert response.status_code == 401
    learn_db.expire_all()
    assert learn_db.query(BillingOrder).filter_by(id=order.id).one().status == "pending"


def test_owned_course_cannot_be_purchased_twice(learn_client, learn_db, learn_catalog, kashier):
    who = register(learn_client)
    course, _, _, _ = _checkout(learn_client, learn_db, kashier, who)
    learn_db.add(CourseEnrollment(user_id=who["id"], course_id=course.id, source="admin_grant", status="active"))
    learn_db.commit()
    response = learn_client.post(
        "/api/v1/billing/checkout", headers=who["headers"], json={"course_id": course.slug},
    )
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "COURSE_ALREADY_OWNED"


def test_course_cannot_have_two_pending_checkouts(learn_client, learn_db, learn_catalog, kashier):
    who = register(learn_client)
    course, _, order, _ = _checkout(learn_client, learn_db, kashier, who)
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


def test_user_cannot_read_another_users_order(learn_client, learn_db, learn_catalog, kashier):
    owner = register(learn_client)
    stranger = register(learn_client)
    _, _, order, _ = _checkout(learn_client, learn_db, kashier, owner)
    assert learn_client.get(f"/api/v1/billing/orders/{order.id}", headers=stranger["headers"]).status_code == 404
