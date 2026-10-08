"""
Migration 018's backfill: people who were already working in a course before
independent enrollment existed appear in "My courses" on day one, and nothing else changes.

The tests insert real legacy rows (tool enrollments, progress on tool topics and on
track levels) and run the migration's own backfill function against them.
"""
import importlib.util
import pathlib
from datetime import datetime, timezone

from app.models.billing import CourseEnrollment
from app.models.learning import Lesson
from app.models.learning_path import Course
from app.models.progress import Enrollment, UserProgress
from app.models.tool_course import ToolEnrollment
from app.models.user import User
from app.services.billing.access_service import course_access
from tests.learning_fixtures import learn_catalog, learn_db, logs_enabled  # noqa: F401

VERSIONS = pathlib.Path(__file__).resolve().parents[1] / "alembic" / "versions"


def _migration():
    spec = importlib.util.spec_from_file_location("m018", VERSIONS / "018_independent_enrollment.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _user(db, n):
    user = User(email=f"backfill-{n}@example.com", hashed_password="x", full_name=f"B{n}")
    db.add(user)
    db.flush()
    return user


def _rows(db, user):
    return {r.course.slug: r for r in db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user.id)}


def test_learners_already_working_in_a_course_are_enrolled_and_nothing_else_is_touched(learn_db, learn_catalog):
    backfill = _migration().backfill_course_enrollments
    langchain = learn_db.query(Course).filter(Course.slug == "langchain").one()
    level_one = learn_db.query(Course).filter(Course.slug == "ai-engineering-foundations").one()
    lesson_of_tool = learn_db.query(Lesson).filter(Lesson.tool_topic_id.isnot(None)).first()
    topic_id, lesson_id = learn_catalog["level_lessons"][1][0]

    # 018's backfill ran, at deploy time, while every course still defaulted
    # to `is_free=true` (021 changed that default afterwards) - so exercising
    # its own SQL here needs that same starting condition made explicit.
    langchain.is_free = True
    level_one.is_free = True
    learn_db.commit()

    enrolled_only, worked_tool, worked_track, track_only, nothing = (_user(learn_db, i) for i in range(5))
    now = datetime(2026, 9, 1, tzinfo=timezone.utc)
    learn_db.add(ToolEnrollment(user_id=enrolled_only.id, tool_course_id=langchain.tool_course_id, enrolled_at=now))
    learn_db.add(ToolEnrollment(user_id=worked_tool.id, tool_course_id=langchain.tool_course_id, enrolled_at=now,
                                progress_pct=100.0, completed_at=now))
    (tool_topic, tool_lesson), = learn_catalog["tool_lessons"]["langchain"]
    learn_db.add(UserProgress(user_id=worked_tool.id, tool_topic_id=tool_topic, lessons_completed=[tool_lesson],
                              started_at=now))
    learn_db.add(UserProgress(user_id=worked_track.id, topic_id=topic_id, lessons_completed=[lesson_id], started_at=now))
    learn_db.add(Enrollment(user_id=track_only.id, track_id=learn_catalog["track"].id))     # a track enrollment alone
    learn_db.commit()
    assert learn_db.query(CourseEnrollment).count() == 0

    backfill(learn_db.connection())
    learn_db.expire_all()

    only = _rows(learn_db, enrolled_only)["langchain"]
    assert (only.source, only.status, only.learning_status, only.started_at) == ("free", "active", "enrolled", None)
    worked = _rows(learn_db, worked_tool)["langchain"]
    assert (worked.learning_status, worked.completed_at is not None, worked.started_at is not None) == ("completed", True, True)
    tracked = _rows(learn_db, worked_track)["ai-engineering-foundations"]
    assert (tracked.source, tracked.learning_status) == ("free", "in_progress")
    assert _rows(learn_db, track_only) == {} and _rows(learn_db, nothing) == {}      # intent alone enrolls no one in every course

    # The rows they already had are exactly as they were.
    assert learn_db.query(ToolEnrollment).count() == 2 and learn_db.query(Enrollment).count() == 1
    assert learn_db.query(UserProgress).filter(UserProgress.user_id == worked_track.id).one().lessons_completed == [lesson_id]

    # Idempotent: running it again adds nothing and changes nothing.
    before = learn_db.query(CourseEnrollment).count()
    backfill(learn_db.connection())
    assert learn_db.query(CourseEnrollment).count() == before


def test_the_backfill_never_overrides_an_existing_enrollment_or_enrolls_in_a_paid_course(learn_db, learn_catalog):
    backfill = _migration().backfill_course_enrollments
    langchain = learn_db.query(Course).filter(Course.slug == "langchain").one()
    qdrant = learn_db.query(Course).filter(Course.slug == "qdrant").one()
    user = _user(learn_db, 9)
    purchased = CourseEnrollment(user_id=user.id, course_id=langchain.id, source="purchase")
    learn_db.add(purchased)
    learn_db.add(ToolEnrollment(user_id=user.id, tool_course_id=langchain.tool_course_id))
    learn_db.add(ToolEnrollment(user_id=user.id, tool_course_id=qdrant.tool_course_id))
    qdrant.is_free = False
    learn_db.commit()

    backfill(learn_db.connection())
    learn_db.expire_all()

    rows = _rows(learn_db, user)
    assert rows["langchain"].source == "purchase"          # the purchase record is left exactly as it was
    assert "qdrant" not in rows                            # a paid course is not enrolled on the learner's behalf


def test_a_backfilled_free_enrollment_does_not_grant_access_to_a_course_that_is_later_paid(learn_db, learn_catalog):
    backfill = _migration().backfill_course_enrollments
    langchain = learn_db.query(Course).filter(Course.slug == "langchain").one()
    user = _user(learn_db, 10)
    learn_db.add(ToolEnrollment(user_id=user.id, tool_course_id=langchain.tool_course_id))
    learn_db.commit()
    backfill(learn_db.connection())
    langchain.is_free = False
    learn_db.commit()
    assert course_access(learn_db, user.id, langchain).has_access is False
