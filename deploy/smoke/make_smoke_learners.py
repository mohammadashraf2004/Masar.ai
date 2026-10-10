"""Create or refresh the controlled AI Mentor smoke learners. Runs inside the api container:

  docker compose --env-file /etc/masar/production.env -f docker-compose.yml -f docker-compose.prod.yml \
      exec -T -e SMOKE_PASSWORD -e SMOKE_PRO=1 api python - < deploy/smoke/make_smoke_learners.py

Idempotent, and touches only the two accounts it names (SMOKE_EMAIL, default
smoke-wallet@example.com; SMOKE_PRO_EMAIL, default smoke-pro@example.com) - never a real learner.

  wallet learner   verified, Free plan, topped up to 80 credits through the ledger (a 'bonus' row,
                   payment method 'admin', so wallets still reconcile), an admin_grant enrollment in
                   course-001 and course-013, and the first two lessons of course-001 complete (the
                   mock interview asks about completed material only)
  Pro learner      with SMOKE_PRO=1: verified, enrolled in course-001, an active Pro subscription
                   (payment_provider 'admin') that ends 24 h from now, so it lapses on its own

SMOKE_CLEANUP=1 instead ends the smoke Pro subscription now and deactivates both accounts.
Prints ids and balances only - never the password.
"""
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.getcwd())

import app.main  # noqa: E402,F401 - every model and relationship registered
from app.core.security import get_password_hash, normalize_email  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.models.billing import BillingPlan, CourseEnrollment, UserSubscription  # noqa: E402
from app.models.learning import Lesson  # noqa: E402
from app.models.learning_path import Course  # noqa: E402
from app.models.progress import UserProgress  # noqa: E402
from app.models.tool_course import ToolCourse, ToolTopic  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.wallet.wallet_service import add_credits, get_or_create_wallet  # noqa: E402

WALLET_EMAIL = normalize_email(os.environ.get("SMOKE_EMAIL", "smoke-wallet@example.com"))
PRO_EMAIL = normalize_email(os.environ.get("SMOKE_PRO_EMAIL", "smoke-pro@example.com"))
TARGET_BALANCE = 80
db = SessionLocal()
now = datetime.now(timezone.utc)


def learner(email):
    user = db.query(User).filter(User.email == email).one_or_none()
    if user is None:
        password = os.environ.get("SMOKE_PASSWORD")
        if not password:
            sys.exit("SMOKE_PASSWORD is required to create the smoke learners")
        user = User(email=email, full_name="Mentor Smoke Test", hashed_password=get_password_hash(password),
                    is_verified=True, is_active=True)
        db.add(user)
        db.commit()
    elif not user.is_active or not user.is_verified:
        user.is_active, user.is_verified = True, True
        db.commit()
    return user


def enroll(user, slug):
    course = db.query(Course).filter(Course.slug == slug).one()
    if not db.query(CourseEnrollment).filter_by(user_id=user.id, course_id=course.id).first():
        db.add(CourseEnrollment(user_id=user.id, course_id=course.id, source="admin_grant", status="active"))
        db.commit()


def complete_first_lessons(user, slug, n=2):
    tool = db.query(ToolCourse).filter(ToolCourse.slug == slug).one()
    topic = db.query(ToolTopic).filter(ToolTopic.tool_course_id == tool.id).order_by(ToolTopic.order).first()
    if db.query(UserProgress).filter_by(user_id=user.id, tool_topic_id=topic.id).first():
        return
    lessons = db.query(Lesson).filter(Lesson.tool_topic_id == topic.id).order_by(Lesson.order).limit(n).all()
    db.add(UserProgress(user_id=user.id, tool_topic_id=topic.id, lessons_completed=[lesson.id for lesson in lessons],
                        exercises_completed=[], started_at=now))
    db.commit()


def top_up(user):
    wallet = get_or_create_wallet(user.id, db)
    if wallet.credit_balance < TARGET_BALANCE:
        add_credits(user.id, TARGET_BALANCE - wallet.credit_balance, db, payment_method="admin",
                    transaction_type="bonus", description="AI Mentor smoke-test learner")
    db.refresh(wallet)
    return wallet.credit_balance


def smoke_subscriptions(user):
    return db.query(UserSubscription).filter(UserSubscription.user_id == user.id,
                                             UserSubscription.payment_provider == "admin",
                                             UserSubscription.provider_subscription_id.like("smoke-%"))


if os.environ.get("SMOKE_CLEANUP") == "1":
    for email in (WALLET_EMAIL, PRO_EMAIL):
        user = db.query(User).filter(User.email == email).one_or_none()
        if user is None:
            continue
        smoke_subscriptions(user).update({UserSubscription.status: "expired", UserSubscription.current_period_end: now},
                                         synchronize_session=False)
        user.is_active = False
        db.commit()
        print(f"deactivated user {user.id}")
    sys.exit(0)

wallet_user = learner(WALLET_EMAIL)
for slug in ("course-001", "course-013"):
    enroll(wallet_user, slug)
complete_first_lessons(wallet_user, "course-001")
print(f"wallet learner {wallet_user.id}: balance {top_up(wallet_user)}")

if os.environ.get("SMOKE_PRO") == "1":
    pro_user = learner(PRO_EMAIL)
    enroll(pro_user, "course-001")
    sub = smoke_subscriptions(pro_user).filter(UserSubscription.status == "active",
                                               UserSubscription.current_period_end > now).first()
    if sub is None:
        plan = db.query(BillingPlan).filter(BillingPlan.code == "pro").one()
        sub = UserSubscription(user_id=pro_user.id, plan_id=plan.id, status="active", billing_period="monthly",
                               payment_provider="admin", provider_subscription_id=f"smoke-{uuid.uuid4().hex[:16]}",
                               current_period_start=now, current_period_end=now + timedelta(hours=24))
        db.add(sub)
        db.commit()
    print(f"Pro learner {pro_user.id}: wallet {get_or_create_wallet(pro_user.id, db).credit_balance}, "
          f"Pro until {sub.current_period_end.isoformat(timespec='minutes')}")
