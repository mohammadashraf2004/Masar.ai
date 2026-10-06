"""
app/services/learning/progress_service.py

Path-aware progress, derived — never stored.

The rule that keeps it honest: **completion belongs to the learner and the
course, not to a path.** A course is finished or it is not, and every path,
career goal and field it appears in sees the same fact. Nothing here writes a
per-path counter, so there is nothing to keep in step and nothing that can
double-count.

How "done" is decided
---------------------
A course's fraction is `completed items / total items` over every lesson and
exercise in its topics, where an item is complete when its id is in the
learner's `lessons_completed` / `exercises_completed` for that topic. That is
exactly the rule the tool-course controller already uses to mark a topic
complete ("every lesson and exercise attached has been marked complete"), so
the two agree.

It is computed from the items rather than read from `UserProgress.status`
because the *track* progress endpoint never sets `status = completed` (and
never writes `Enrollment.completion_percentage`), so for a track level that
column would say "in progress" forever. A tool course that carries a
`ToolCourseCompletion` row — the credential — is complete regardless.

Quizzes and projects do not count toward completion, matching the existing
rule; they are assessments, not required reading.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from sqlalchemy.orm import Session

from app.models.learning import Exercise, Lesson, Topic
from app.models.learning_path import COURSE_KIND_TOOL, COURSE_KIND_TRACK_LEVEL, Course
from app.models.progress import UserProgress
from app.models.tool_course import ToolCourseCompletion, ToolTopic
from app.services.learning.domain import (
    COUNTED_STATES, STATE_COMPLETED, STATE_WAIVED, Catalog,
)

# Percentages are reported to one decimal; a fraction at or above this counts
# as finished. Fractions are exact ratios of small integers, so this only
# guards float noise.
_DONE = 1.0 - 1e-9


def _fractions(
    topic_owner: Dict[int, int],
    lessons: Sequence[Tuple[int, int]],
    exercises: Sequence[Tuple[int, int]],
    progress: Dict[int, UserProgress],
) -> Dict[int, float]:
    """Fraction of items done per content source (a tool course or a level)."""
    total: Dict[int, int] = {}
    done: Dict[int, int] = {}

    def tally(items: Sequence[Tuple[int, int]], completed_of) -> None:
        for item_id, topic_id in items:
            owner = topic_owner[topic_id]
            total[owner] = total.get(owner, 0) + 1
            row = progress.get(topic_id)
            if row is not None and item_id in completed_of(row):
                done[owner] = done.get(owner, 0) + 1

    tally(lessons, lambda r: set(r.lessons_completed or []))
    tally(exercises, lambda r: set(r.exercises_completed or []))
    return {owner: done.get(owner, 0) / count for owner, count in total.items() if count}


def course_completion(db: Session, user_id: int, courses: Iterable[Course]) -> Dict[int, float]:
    """Completion fraction (0.0-1.0) for each course, in a fixed number of
    queries regardless of how many courses are asked about."""
    courses = list(courses)
    result: Dict[int, float] = {c.id: 0.0 for c in courses}

    tool_courses = {c.tool_course_id: c.id for c in courses if c.kind == COURSE_KIND_TOOL and c.tool_course_id}
    levels = {c.track_level_id: c.id for c in courses if c.kind == COURSE_KIND_TRACK_LEVEL and c.track_level_id}

    if tool_courses:
        topics = db.query(ToolTopic.id, ToolTopic.tool_course_id).filter(
            ToolTopic.tool_course_id.in_(list(tool_courses)),
            ToolTopic.completion_required.is_(True),
        ).all()
        owner = {tid: cid for tid, cid in topics}
        if owner:
            lessons = db.query(Lesson.id, Lesson.tool_topic_id).filter(Lesson.tool_topic_id.in_(list(owner))).all()
            exercises = db.query(Exercise.id, Exercise.tool_topic_id).filter(Exercise.tool_topic_id.in_(list(owner))).all()
            progress = {
                p.tool_topic_id: p for p in db.query(UserProgress).filter(
                    UserProgress.user_id == user_id, UserProgress.tool_topic_id.in_(list(owner)),
                ).all()
            }
            for src, frac in _fractions(owner, lessons, exercises, progress).items():
                result[tool_courses[src]] = frac
        credentials = {
            row[0] for row in db.query(ToolCourseCompletion.tool_course_id).filter(
                ToolCourseCompletion.user_id == user_id,
                ToolCourseCompletion.tool_course_id.in_(list(tool_courses)),
            ).all()
        }
        for src in credentials:
            result[tool_courses[src]] = 1.0

    if levels:
        topics = db.query(Topic.id, Topic.level_id).filter(Topic.level_id.in_(list(levels))).all()
        owner = {tid: lid for tid, lid in topics}
        if owner:
            lessons = db.query(Lesson.id, Lesson.topic_id).filter(Lesson.topic_id.in_(list(owner))).all()
            exercises = db.query(Exercise.id, Exercise.topic_id).filter(Exercise.topic_id.in_(list(owner))).all()
            progress = {
                p.topic_id: p for p in db.query(UserProgress).filter(
                    UserProgress.user_id == user_id, UserProgress.topic_id.in_(list(owner)),
                ).all()
            }
            for src, frac in _fractions(owner, lessons, exercises, progress).items():
                result[levels[src]] = frac

    return result


def resolve_state(state: str, fraction: float) -> str:
    """A planned course's state once the learner's progress is known: a course
    they have finished reads as completed wherever the saved snapshot still says
    required. A course they said they already know stays that way."""
    return STATE_COMPLETED if state != STATE_WAIVED and fraction >= _DONE else state


def completed_course_ids(completion: Dict[int, float]) -> Set[int]:
    return {cid for cid, frac in completion.items() if frac >= _DONE}


def pct(fraction: float) -> float:
    return round(100.0 * fraction, 1)


def stage_progress(
    courses: Sequence[Tuple[int, str]],
    completion: Dict[int, float],
) -> Optional[float]:
    """Progress of one stage from its `(course_id, state)` pairs.

    Only required and completed courses count; optional and waived ones are
    visible but never in the denominator, so skipping one cannot lower a
    percentage. None means "nothing here to measure" (an empty or all-optional
    stage), which the UI presents as coming soon / skippable — never as 0%.
    """
    counted = [(cid, state) for cid, state in courses if state in COUNTED_STATES]
    if not counted:
        return None
    fractions = [1.0 if state == STATE_COMPLETED else completion.get(cid, 0.0) for cid, state in counted]
    return pct(sum(fractions) / len(fractions))


def overview(
    catalog: Catalog,
    completion: Dict[int, float],
    path_course_ids: Iterable[int] = (),
) -> Dict[str, object]:
    """Overall progress plus the per-career-goal, per-field and per-skill views.

    `overall_pct` is the mean over the courses the learner is engaged with —
    everything on their path plus anything they have started elsewhere — with
    each course counted exactly once. It is deliberately *not* a share of the
    whole catalogue, which would read as 3% for someone halfway through the
    only path they chose.

    `by_*` answer "how far along am I in X?": the mean completion of the
    available courses tagged X. A course tagged with three fields contributes
    to each of the three, and to none of them twice.
    """
    available = {cid: c for cid, c in catalog.courses.items() if c.is_available}

    engaged: Set[int] = {cid for cid in path_course_ids if cid in available}
    engaged |= {cid for cid, frac in completion.items() if cid in available and frac > 0}
    overall = pct(sum(completion.get(cid, 0.0) for cid in engaged) / len(engaged)) if engaged else 0.0

    def mean_by(key) -> Dict[str, float]:
        buckets: Dict[str, List[float]] = {}
        for cid, course in available.items():
            for slug in key(course):
                buckets.setdefault(slug, []).append(completion.get(cid, 0.0))
        return {slug: pct(sum(v) / len(v)) for slug, v in sorted(buckets.items())}

    return {
        "overall_pct": overall,
        "by_role": mean_by(lambda c: c.role_slugs),
        "by_field": mean_by(lambda c: c.field_slugs),
        "by_skill": mean_by(lambda c: c.teaches),
    }
