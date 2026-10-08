"""
The post-seed legacy-enrollment backfill (release 2026-10-08).

Production comes from before migration 011, so when 018 and 021 run inside
`alembic upgrade head` the course catalogue is still empty and neither finds a
learner to carry over. `backfill_legacy_enrollments` runs after the seeds and
gives every pre-launch learner an active `legacy_free` enrollment in each course
they were already working in - and nothing else.

These tests build the state that step meets: a seeded catalogue at head (every
course `is_free = false`), legacy tool enrollments and progress, and no
course enrollments at all.
"""
from datetime import datetime, timedelta, timezone

import pytest

from app.models.billing import CourseEnrollment, CourseEnrollmentLegacyFree
from app.models.learning_path import Course
from app.models.progress import Enrollment, UserProgress
from app.models.tool_course import ToolEnrollment
from app.models.user import User
from app.services.billing.access_service import course_access
from app.services.billing.legacy_enrollments import backfill_legacy_enrollments
from tests.learning_fixtures import learn_catalog, learn_db, logs_enabled  # noqa: F401

PRE_LAUNCH = datetime(2026, 9, 1, tzinfo=timezone.utc)
CUTOFF = datetime(2026, 10, 1, tzinfo=timezone.utc)        # "the release window began"
AFTER = datetime(2026, 10, 5, tzinfo=timezone.utc)


def _user(db, n, created_at=PRE_LAUNCH):
    user = User(email=f"legacy-{n}@example.com", hashed_password="x", full_name=f"L{n}", created_at=created_at)
    db.add(user)
    db.flush()
    return user


def _rows(db, user):
    return {r.course.slug: r for r in db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user.id)}


@pytest.fixture()
def courses(learn_db, learn_catalog):
    langchain = learn_db.query(Course).filter(Course.slug == "langchain").one()
    qdrant = learn_db.query(Course).filter(Course.slug == "qdrant").one()
    level_one = learn_db.query(Course).filter(Course.slug == "ai-engineering-foundations").one()
    assert not (langchain.is_free or qdrant.is_free or level_one.is_free), "021 leaves every course paid"
    return langchain, qdrant, level_one


def test_pre_launch_learners_keep_the_courses_they_were_taking(learn_db, learn_catalog, courses):
    langchain, qdrant, level_one = courses
    topic_id, lesson_id = learn_catalog["level_lessons"][1][0]
    (tool_topic, tool_lesson), = learn_catalog["tool_lessons"]["langchain"]
    enrolled_only, worked_tool, worked_track, track_only, nothing = (_user(learn_db, i) for i in range(5))
    learn_db.add_all([
        ToolEnrollment(user_id=enrolled_only.id, tool_course_id=langchain.tool_course_id, enrolled_at=PRE_LAUNCH),
        ToolEnrollment(user_id=worked_tool.id, tool_course_id=langchain.tool_course_id, enrolled_at=PRE_LAUNCH,
                       progress_pct=100.0, completed_at=PRE_LAUNCH),
        UserProgress(user_id=worked_tool.id, tool_topic_id=tool_topic, lessons_completed=[tool_lesson],
                     started_at=PRE_LAUNCH),
        UserProgress(user_id=worked_track.id, topic_id=topic_id, lessons_completed=[lesson_id], started_at=PRE_LAUNCH),
        Enrollment(user_id=track_only.id, track_id=learn_catalog["track"].id),       # a career goal, not a course
    ])
    learn_db.commit()
    assert learn_db.query(CourseEnrollment).count() == 0
    for user, course in ((enrolled_only, langchain), (worked_tool, langchain), (worked_track, level_one)):
        assert not course_access(learn_db, user.id, course).has_access     # the bug: locked out after 021

    report = backfill_legacy_enrollments(learn_db, CUTOFF)
    learn_db.commit()
    learn_db.expire_all()

    assert report == {"pairs": 3, "created": 3, "grandfathered": 3, "already_entitled": 0, "left_inactive": 0}
    only = _rows(learn_db, enrolled_only)["langchain"]
    assert (only.source, only.status, only.learning_status) == ("legacy_free", "active", "enrolled")
    worked = _rows(learn_db, worked_tool)["langchain"]
    assert (worked.source, worked.learning_status, worked.started_at is not None) == ("legacy_free", "completed", True)
    assert _rows(learn_db, worked_track)["ai-engineering-foundations"].source == "legacy_free"
    assert _rows(learn_db, track_only) == {} and _rows(learn_db, nothing) == {}
    for user, course in ((enrolled_only, langchain), (worked_tool, langchain), (worked_track, level_one)):
        access = course_access(learn_db, user.id, course)
        assert access.has_access and access.reason == "legacy_free"
    assert not course_access(learn_db, enrolled_only.id, qdrant).has_access        # only what they were taking

    # Recorded like 021's own grandfathering, so its downgrade restores `free`.
    legacy = learn_db.query(CourseEnrollmentLegacyFree).all()
    assert sorted((r.user_id, r.previous_source) for r in legacy) == sorted(
        (u.id, "free") for u in (enrolled_only, worked_tool, worked_track))

    # The legacy rows themselves are exactly as they were.
    assert learn_db.query(ToolEnrollment).count() == 2 and learn_db.query(Enrollment).count() == 1
    assert learn_db.query(UserProgress).filter(UserProgress.user_id == worked_track.id).one().lessons_completed == [lesson_id]

    # Idempotent.
    again = backfill_legacy_enrollments(learn_db, CUTOFF)
    assert (again["created"], again["grandfathered"], again["already_entitled"]) == (0, 0, 3)
    assert learn_db.query(CourseEnrollment).count() == 3 and learn_db.query(CourseEnrollmentLegacyFree).count() == 3


def test_existing_enrollments_are_respected(learn_db, learn_catalog, courses):
    langchain, qdrant, _ = courses
    buyer, enrolled_since, revoked = (_user(learn_db, 10 + i) for i in range(3))
    for user in (buyer, enrolled_since, revoked):
        learn_db.add(ToolEnrollment(user_id=user.id, tool_course_id=langchain.tool_course_id, enrolled_at=PRE_LAUNCH))
    learn_db.add_all([
        CourseEnrollment(user_id=buyer.id, course_id=langchain.id, source="purchase", status="active"),
        CourseEnrollment(user_id=enrolled_since.id, course_id=langchain.id, source="free", status="active"),
        CourseEnrollment(user_id=revoked.id, course_id=langchain.id, source="free", status="revoked"),
    ])
    learn_db.commit()

    report = backfill_legacy_enrollments(learn_db, CUTOFF)
    learn_db.expire_all()

    assert report == {"pairs": 3, "created": 0, "grandfathered": 1, "already_entitled": 1, "left_inactive": 1}
    assert _rows(learn_db, buyer)["langchain"].source == "purchase"                  # untouched
    assert _rows(learn_db, enrolled_since)["langchain"].source == "legacy_free"      # a free enrollment is upgraded
    gone = _rows(learn_db, revoked)["langchain"]
    assert (gone.source, gone.status) == ("free", "revoked")                          # not revived


def test_nothing_from_the_release_window_onwards_counts(learn_db, learn_catalog, courses):
    langchain, _, _ = courses
    (tool_topic, tool_lesson), = learn_catalog["tool_lessons"]["langchain"]
    new_account = _user(learn_db, 20, created_at=AFTER)
    old_account_new_course = _user(learn_db, 21)
    old_account_new_progress = _user(learn_db, 22)
    learn_db.add_all([
        ToolEnrollment(user_id=new_account.id, tool_course_id=langchain.tool_course_id, enrolled_at=AFTER),
        ToolEnrollment(user_id=old_account_new_course.id, tool_course_id=langchain.tool_course_id, enrolled_at=AFTER),
        UserProgress(user_id=old_account_new_progress.id, tool_topic_id=tool_topic, lessons_completed=[tool_lesson],
                     started_at=AFTER),
    ])
    learn_db.commit()

    report = backfill_legacy_enrollments(learn_db, CUTOFF)
    assert report["pairs"] == 0 and report["created"] == 0
    assert learn_db.query(CourseEnrollment).count() == 0


@pytest.mark.parametrize("cutoff, message", [
    (datetime(2026, 10, 1), "timezone"),
    (datetime.now(timezone.utc) + timedelta(days=1), "future"),
])
def test_the_cutoff_must_be_explicit_and_in_the_past(learn_db, cutoff, message):
    with pytest.raises(ValueError, match=message):
        backfill_legacy_enrollments(learn_db, cutoff)
