"""Free -> Pro pricing, access, migration, and subscription settlement."""
from datetime import datetime, timedelta, timezone
import hashlib
import hmac as hmac_lib
import uuid

from app.models.billing import BillingPlan, SubscriptionOrder, SubscriptionPaymentEvent, UserSubscription
from app.models.learning import Lesson
from app.models.wallet import TransactionStatus, TransactionType, UserWallet, WalletTransaction
from app.services.payments import paymob_service
from app.services.learning.catalog_service import load_catalog_bundle
from app.services.wallet.wallet_service import add_credits, migrate_free_wallets_to_40
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register


SECRET = "subscription-webhook-secret"


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _register(client):
    email = f"monetization-{uuid.uuid4().hex[:12]}@example.com"
    response = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Monetization Test",
        "password": "correct-horse-battery-staple-7",
        "accept_terms": True, "accept_privacy": True,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    return body["user"]["id"], body["access_token"]


def _sign(obj: dict) -> str:
    concatenated = "".join(
        paymob_service._stringify(paymob_service._extract(obj, field))
        for field in paymob_service._HMAC_FIELDS
    )
    return hmac_lib.new(SECRET.encode(), concatenated.encode(), hashlib.sha512).hexdigest()


def _event(order: SubscriptionOrder, event_id: int, *, success: bool = True) -> dict:
    return {
        "amount_cents": order.amount, "created_at": "2026-09-27T12:00:00.000000",
        "currency": order.currency, "error_occured": False, "has_parent_transaction": False,
        "id": event_id, "integration_id": 123, "is_3d_secure": True, "is_auth": False,
        "is_capture": False, "is_refunded": False, "is_standalone_payment": True,
        "is_voided": False,
        "order": {"id": int(order.provider_order_id), "merchant_order_id": order.merchant_order_id},
        "owner": 42, "pending": False,
        "source_data": {"pan": "1234", "sub_type": "MasterCard", "type": "card"},
        "success": success,
    }


def test_backend_catalog_is_authoritative_egp_pricing(client):
    body = client.get("/api/v1/billing/catalog").json()
    assert body["currency"] == "EGP"
    plans = {plan["id"]: plan for plan in body["plans"]}
    assert plans["free"]["signup_credits"] == 40
    assert plans["pro"]["monthly"] == 299
    assert plans["pro"]["yearly"] == 2199
    assert plans["pro"]["signup_credits"] == 0


def test_free_balance_normalizer_is_idempotent_and_preserves_history_and_buyers(client, db):
    """Approved policy (2026-10-07): a floor of 40, never a reset - a free balance above 40 is kept."""
    free_id, _ = _register(client)
    low_id, _ = _register(client)
    paid_id, _ = _register(client)
    free_wallet = db.query(UserWallet).filter_by(user_id=free_id).one()
    low_wallet = db.query(UserWallet).filter_by(user_id=low_id).one()
    low_wallet.credit_balance = 12
    paid_wallet = db.query(UserWallet).filter_by(user_id=paid_id).one()

    historical = WalletTransaction(
        wallet_id=free_wallet.id, transaction_type=TransactionType.deduction,
        status=TransactionStatus.confirmed, credits=-2, description="Historical mentor use",
        action_type="mentor_chat", balance_after=38,
    )
    db.add(historical)
    free_wallet.credit_balance = 123
    db.commit()
    add_credits(paid_id, 100, db, egp_amount=50, description="Paid pack")
    paid_wallet = db.query(UserWallet).filter_by(user_id=paid_id).one()
    paid_wallet.credit_balance = 777
    db.commit()

    before_history = db.query(WalletTransaction).filter_by(wallet_id=free_wallet.id).count()
    # `db`/`client` share the suite's real database rather than a per-test
    # rollback, so other tests' students may already be sitting there
    # unmigrated - only the *first* call's count is order-dependent. The
    # idempotency claim is the second call doing nothing at all.
    assert migrate_free_wallets_to_40(db) >= 1
    assert migrate_free_wallets_to_40(db) == 0

    db.refresh(free_wallet)
    db.refresh(low_wallet)
    db.refresh(paid_wallet)
    assert free_wallet.credit_balance == 123  # above the floor: never reduced
    assert low_wallet.credit_balance == 40    # below it: raised
    assert paid_wallet.credit_balance == 777
    assert db.query(WalletTransaction).filter_by(wallet_id=free_wallet.id).count() == before_history
    assert db.query(WalletTransaction).filter_by(id=historical.id).one().credits == -2
    marker = WalletTransaction.action_type == "free_plan_40_migration_v1"
    assert db.query(WalletTransaction).filter(WalletTransaction.wallet_id == free_wallet.id, marker).count() == 0
    raised = db.query(WalletTransaction).filter(WalletTransaction.wallet_id == low_wallet.id, marker).all()
    assert [r.credits for r in raised] == [28]


def test_free_gets_first_two_lessons_but_direct_third_lesson_progress_is_denied(
    learn_client, learn_db, learn_catalog,
):
    who = register(learn_client)
    bundle = load_catalog_bundle(learn_db)
    course = next(
        c for c in bundle.courses.values()
        if c.tool_course_id and any(topic.lessons for topic in c.tool_course.topics)
    )
    topic = next(topic for topic in course.tool_course.topics if topic.lessons)
    highest = max((lesson.order for lesson in topic.lessons), default=0)
    learn_db.add_all([
        Lesson(tool_topic_id=topic.id, title="Free preview two", content="two", order=highest + 1),
        Lesson(tool_topic_id=topic.id, title="Locked lesson three", content="three", order=highest + 2),
    ])
    learn_db.commit()
    response = learn_client.get(f"/api/v1/tool-courses/{course.tool_course.slug}", headers=who["headers"])
    assert response.status_code == 200
    lessons = [lesson for topic in response.json()["topics"] for lesson in topic["lessons"]]
    assert lessons[0]["content"] and lessons[1]["content"]
    assert lessons[0]["is_locked"] is False and lessons[1]["is_locked"] is False
    assert lessons[2]["content"] == "" and lessons[2]["is_locked"] is True

    third_topic = next(topic for topic in response.json()["topics"] if any(l["id"] == lessons[2]["id"] for l in topic["lessons"]))
    denied = learn_client.post(
        f"/api/v1/tool-courses/topics/{third_topic['id']}/progress",
        headers=who["headers"], json={"lesson_id": lessons[2]["id"]},
    )
    assert denied.status_code == 403
    assert denied.json()["detail"]["code"] == "COURSE_PURCHASE_REQUIRED"


def test_active_and_cancelled_pro_have_access_until_expiry_then_return_to_free(
    learn_client, learn_db, learn_catalog,
):
    who = register(learn_client)
    plan = learn_db.query(BillingPlan).filter_by(code="pro").one()
    now = datetime.now(timezone.utc)
    subscription = UserSubscription(
        user_id=who["id"], plan_id=plan.id, status="active", billing_period="monthly",
        payment_provider="test", provider_subscription_id=f"sub-{uuid.uuid4().hex}",
        current_period_start=now, current_period_end=now + timedelta(days=30),
    )
    learn_db.add(subscription)
    learn_db.commit()
    bundle = load_catalog_bundle(learn_db)
    course = next(c for c in bundle.courses.values() if c.tool_course_id)

    access = learn_client.get(f"/api/v1/learning/courses/{course.slug}/access", headers=who["headers"])
    assert access.json()["has_access"] is True and access.json()["reason"] == "pro"

    cancelled = learn_client.post("/api/v1/billing/subscription/cancel", headers=who["headers"])
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert cancelled.json()["has_pro_access"] is True

    subscription.current_period_end = now - timedelta(seconds=1)
    learn_db.commit()
    expired = learn_client.get(f"/api/v1/learning/courses/{course.slug}/access", headers=who["headers"])
    assert expired.json()["has_access"] is False


def test_subscription_webhook_is_idempotent_and_failed_payment_grants_nothing(client, db, monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    user_id, _ = _register(client)
    plan = db.query(BillingPlan).filter_by(code="pro").one()
    order = SubscriptionOrder(
        user_id=user_id, plan_id=plan.id, billing_period="monthly", amount=29900,
        currency="EGP", provider="paymob", merchant_order_id=f"subscription-{uuid.uuid4().hex}",
        provider_order_id="88101", status="pending",
    )
    db.add(order)
    db.commit()

    obj = _event(order, 99101)
    first = client.post(f"/api/v1/payments/paymob/webhook?hmac={_sign(obj)}", json={"obj": obj})
    second = client.post(f"/api/v1/payments/paymob/webhook?hmac={_sign(obj)}", json={"obj": obj})
    assert first.json()["success"] is True
    assert second.json()["status"] == "already_processed"
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=order.id).count() == 1
    assert db.query(UserSubscription).filter_by(user_id=user_id).count() == 1

    other_id, _ = _register(client)
    failed_order = SubscriptionOrder(
        user_id=other_id, plan_id=plan.id, billing_period="yearly", amount=219900,
        currency="EGP", provider="paymob", merchant_order_id=f"subscription-{uuid.uuid4().hex}",
        provider_order_id="88102", status="pending",
    )
    db.add(failed_order)
    db.commit()
    failed_obj = _event(failed_order, 99102, success=False)
    failed = client.post(f"/api/v1/payments/paymob/webhook?hmac={_sign(failed_obj)}", json={"obj": failed_obj})
    assert failed.json()["success"] is False
    assert db.query(UserSubscription).filter_by(user_id=other_id).count() == 0
