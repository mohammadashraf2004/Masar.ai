"""
Migration 021's data policy (release decision 2026-10-07), on a real database:

* wallets of eligible free students are raised to at least 40, never reduced, with one
  ledger row per raised wallet; a second run changes nothing;
* a learner enrolled while a course was free keeps it (`legacy_free`), nobody else gains
  access, and every course's previous `is_free` is kept in `course_free_legacy`;
* downgrading 021 restores the free flags and enrollment sources exactly.

The scenario is built at head, the database is taken back to 020 and given the pre-launch
state, then 021 is applied.

Migration 021 runs on its own connections, so the scenario has to be committed. The
fixtures below remove it again afterwards, pass or fail, and undo what 021 did to rows
the test did not create, so no other test sees any of it whatever order they run in.
"""
import uuid

import pytest
import sqlalchemy as sa
from alembic import command

from app.db.session import engine
from app.models.learning_path import Course, LearningLevel
from app.models.tool_course import ToolCourse
from app.models.user import User
from tests.test_migration_graph import _config

MARK = "free_plan_40_migration_v1"


@pytest.fixture()
def created(db):
    """Ids of the rows a test creates; deleted afterwards, children before parents."""
    ids = {"users": [], "courses": [], "tool_courses": [], "learning_levels": []}
    yield ids
    db.rollback()
    with engine.begin() as conn:
        for sql in (
            "DELETE FROM wallet_transactions WHERE wallet_id IN "
            "(SELECT id FROM user_wallets WHERE user_id = ANY(:users))",
            "DELETE FROM user_wallets WHERE user_id = ANY(:users)",
            # course_enrollment_legacy_free and course_free_legacy rows cascade.
            "DELETE FROM course_enrollments WHERE user_id = ANY(:users) OR course_id = ANY(:courses)",
            "DELETE FROM users WHERE id = ANY(:users)",
            "DELETE FROM courses WHERE id = ANY(:courses)",
            "DELETE FROM tool_courses WHERE id = ANY(:tool_courses)",
            "DELETE FROM learning_levels WHERE id = ANY(:learning_levels)",
        ):
            conn.execute(sa.text(sql), ids)


# What 021 writes outside the scenario: it raises every eligible wallet in the database,
# creates missing ones, clears every course's is_free, re-sources free enrollments, and
# the downgrade/upgrade rebuilds both legacy tables from the current catalogue.
_SNAPSHOT = {
    "user_wallets": "SELECT id, credit_balance, promo_credits_remaining, promo_expires_at, updated_at "
                    "FROM user_wallets",
    "courses": "SELECT id, is_free FROM courses",
    "course_enrollments": "SELECT id, source FROM course_enrollments",
    "course_free_legacy": "SELECT course_id, was_free, recorded_at FROM course_free_legacy",
    "course_enrollment_legacy_free": "SELECT enrollment_id, user_id, course_id, previous_source, granted_at "
                                     "FROM course_enrollment_legacy_free",
}
_RESTORE = {
    "user_wallets": "UPDATE user_wallets SET credit_balance = :credit_balance, "
                    "promo_credits_remaining = :promo_credits_remaining, promo_expires_at = :promo_expires_at, "
                    "updated_at = :updated_at WHERE id = :id",
    "courses": "UPDATE courses SET is_free = :is_free WHERE id = :id",
    "course_enrollments": "UPDATE course_enrollments SET source = :source WHERE id = :id",
}


@pytest.fixture()
def restores_021_side_effects():
    """Puts back every row 021 changed that existed before the test, and removes the
    wallets and ledger rows it added. Runs after the test has returned to head."""
    with engine.connect() as conn:
        last_transaction = conn.execute(sa.text("SELECT COALESCE(max(id), 0) FROM wallet_transactions")).scalar()
        before = {table: [dict(r._mapping) for r in conn.execute(sa.text(sql))] for table, sql in _SNAPSHOT.items()}
    yield
    with engine.begin() as conn:
        conn.execute(sa.text("DELETE FROM wallet_transactions WHERE id > :last"), {"last": last_transaction})
        conn.execute(sa.text("DELETE FROM user_wallets WHERE NOT (id = ANY(:kept))"),
                     {"kept": [w["id"] for w in before["user_wallets"]]})
        for table, sql in _RESTORE.items():
            now = {r["id"]: r for r in (dict(r._mapping) for r in conn.execute(sa.text(_SNAPSHOT[table])))}
            changed = [r for r in before[table] if r["id"] in now and now[r["id"]] != r]
            if changed:
                conn.execute(sa.text(sql), changed)
        for table in ("course_enrollment_legacy_free", "course_free_legacy"):
            conn.execute(sa.text(f"DELETE FROM {table}"))
            if before[table]:
                columns = list(before[table][0])
                conn.execute(sa.text(f"INSERT INTO {table} ({', '.join(columns)}) "
                                     f"VALUES ({', '.join(':' + c for c in columns)})"), before[table])


def _course(db, tag, created):
    level = LearningLevel(slug=f"lvl-{tag}", name=f"Level {tag}", rank=10_000 + uuid.uuid4().int % 10**6)
    tool = ToolCourse(slug=f"tool-{tag}", title=f"Tool {tag}")
    db.add_all([level, tool])
    db.flush()
    course = Course(slug=f"course-{tag}", kind="tool_course", tool_course_id=tool.id, level_id=level.id)
    db.add(course)
    db.flush()
    created["learning_levels"].append(level.id)
    created["tool_courses"].append(tool.id)
    created["courses"].append(course.id)
    return course.id


def _student(db, tag, created):
    user = User(email=f"m021-{tag}-{uuid.uuid4().hex[:8]}@example.com", full_name=tag, hashed_password="x")
    db.add(user)
    db.flush()
    created["users"].append(user.id)
    return user.id


def _rows(conn, sql, **kw):
    return conn.execute(sa.text(sql), kw).all()


def test_021_raises_never_reduces_and_grandfathers_reversibly(db, restores_021_side_effects, created):
    tag = uuid.uuid4().hex[:8]
    free_course, paid_course = _course(db, f"free-{tag}", created), _course(db, f"paid-{tag}", created)
    users = {name: _student(db, f"{name}-{tag}", created) for name in
             ("zero", "ten", "forty", "granted75", "payer", "enrolled", "previewer", "lapsed", "buyer")}
    db.commit()

    cfg = _config()
    try:
        command.downgrade(cfg, "020_user_tours")
        with engine.begin() as conn:
            conn.execute(sa.text("UPDATE courses SET is_free = (id = :free) WHERE id IN (:free, :paid)"),
                         {"free": free_course, "paid": paid_course})
            for name, balance in (("zero", 0), ("ten", 10), ("forty", 40), ("granted75", 75), ("payer", 5)):
                conn.execute(sa.text(
                    "INSERT INTO user_wallets (user_id, credit_balance, lifetime_purchased, lifetime_spent, "
                    "promo_credits_remaining, is_active) VALUES (:u, :b, 0, 0, 0, true) "
                    "ON CONFLICT (user_id) DO UPDATE SET credit_balance = :b"), {"u": users[name], "b": balance})
            conn.execute(sa.text(
                "INSERT INTO wallet_transactions (wallet_id, transaction_type, status, credits, payment_method, "
                "description, balance_after) SELECT id, 'topup', 'confirmed', 5, 'card', 'bought', 5 "
                "FROM user_wallets WHERE user_id = :u"), {"u": users["payer"]})
            for name, course, source, status in (
                ("enrolled", free_course, "free", "active"),     # enrolled while free -> keeps it
                ("previewer", paid_course, "free", "active"),    # preview of a paid course -> unchanged
                ("lapsed", free_course, "free", "revoked"),      # no live enrollment -> unchanged
                ("buyer", free_course, "purchase", "active"),    # already entitled -> unchanged
            ):
                conn.execute(sa.text(
                    "INSERT INTO course_enrollments (user_id, course_id, source, status) VALUES (:u, :c, :s, :st)"),
                    {"u": users[name], "c": course, "s": source, "st": status})

        command.upgrade(cfg, "021_free_pro_subscriptions")
        with engine.connect() as conn:
            balances = dict(_rows(conn, "SELECT u.id, w.credit_balance FROM user_wallets w JOIN users u ON u.id = w.user_id "
                                         "WHERE u.id = ANY(:ids)", ids=list(users.values())))
            assert balances[users["zero"]] == 40 and balances[users["ten"]] == 40
            assert balances[users["forty"]] == 40 and balances[users["granted75"]] == 75
            assert balances[users["payer"]] == 5
            ledger = dict(_rows(conn, "SELECT w.user_id, t.credits FROM wallet_transactions t JOIN user_wallets w "
                                      "ON w.id = t.wallet_id WHERE t.action_type = :m AND w.user_id = ANY(:ids)",
                                m=MARK, ids=list(users.values())))
            # Students with no wallet get one (at 0) and are raised like everyone else under 40;
            # 40 and 75 are untouched, the payer and the course buyer are not eligible.
            assert ledger == {users["zero"]: 40, users["ten"]: 30, users["enrolled"]: 40,
                              users["previewer"]: 40, users["lapsed"]: 40}
            sources = dict(_rows(conn, "SELECT user_id, source FROM course_enrollments WHERE user_id = ANY(:ids)",
                                 ids=list(users.values())))
            assert sources == {users["enrolled"]: "legacy_free", users["previewer"]: "free",
                               users["lapsed"]: "free", users["buyer"]: "purchase"}
            assert _rows(conn, "SELECT course_id, was_free FROM course_free_legacy WHERE course_id IN (:f, :p) "
                               "ORDER BY course_id", f=free_course, p=paid_course) == sorted(
                [(free_course, True), (paid_course, False)])
            assert _rows(conn, "SELECT user_id, previous_source FROM course_enrollment_legacy_free WHERE course_id = :f",
                         f=free_course) == [(users["enrolled"], "free")]
            assert _rows(conn, "SELECT is_free FROM courses WHERE id = :f", f=free_course) == [(False,)]
            ledger_rows = conn.execute(sa.text("SELECT count(*) FROM wallet_transactions WHERE action_type = :m"),
                                       {"m": MARK}).scalar()

        # Downgrade restores the catalogue flags and the enrollment sources exactly...
        command.downgrade(cfg, "020_user_tours")
        with engine.connect() as conn:
            assert _rows(conn, "SELECT is_free FROM courses WHERE id = :f", f=free_course) == [(True,)]
            assert _rows(conn, "SELECT source FROM course_enrollments WHERE user_id = :u",
                         u=users["enrolled"]) == [("free",)]
        # ...and running 021 a second time changes no wallet and adds no ledger row.
        command.upgrade(cfg, "021_free_pro_subscriptions")
        with engine.connect() as conn:
            again = dict(_rows(conn, "SELECT u.id, w.credit_balance FROM user_wallets w JOIN users u ON u.id = w.user_id "
                                      "WHERE u.id = ANY(:ids)", ids=list(users.values())))
            assert again == balances
            assert conn.execute(sa.text("SELECT count(*) FROM wallet_transactions WHERE action_type = :m"),
                                {"m": MARK}).scalar() == ledger_rows
            assert _rows(conn, "SELECT source FROM course_enrollments WHERE user_id = :u",
                         u=users["enrolled"]) == [("legacy_free",)]
    finally:
        command.upgrade(cfg, "head")


def test_a_grandfathered_enrollment_grants_access_and_a_preview_does_not(db, created):
    from app.models.billing import CourseEnrollment
    from app.services.billing.access_service import course_access

    tag = uuid.uuid4().hex[:8]
    course = db.get(Course, _course(db, f"acc-{tag}", created))
    kept, previewer = _student(db, f"kept-{tag}", created), _student(db, f"prev-{tag}", created)
    db.add_all([CourseEnrollment(user_id=kept, course_id=course.id, source="legacy_free", status="active"),
                CourseEnrollment(user_id=previewer, course_id=course.id, source="free", status="active")])
    db.commit()
    assert course_access(db, kept, course).has_access
    assert course_access(db, kept, course).reason == "legacy_free"
    assert not course_access(db, previewer, course).has_access
    db.query(CourseEnrollment).filter(CourseEnrollment.course_id == course.id).delete()
    db.commit()
