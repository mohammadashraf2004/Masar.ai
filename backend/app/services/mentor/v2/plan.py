"""The weekly study plan, built from the learner's real Masar state.

It used to be a paid model call that knew only a track name and the account's level: it was
generated (and charged) every time the tab opened, and its days pointed at no real lesson.
The plan is now arithmetic over records - active enrolments, the canonical lesson order, the
lessons already completed, what the learner may open, the lessons' estimated minutes and the
quiz evidence - so it is free, deterministic, and every block names a lesson that exists.
Nothing is invented: with no enrolment the plan says so and is empty.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.services.mentor import learner_state
from app.services.mentor.v2 import skills as skill_model

DAILY_MINUTES = 60
STUDY_DAYS = 6          # Saturday to Thursday; the seventh day (Friday) is left free
MIN_BLOCK_MINUTES = 15
DEFAULT_LESSON_MINUTES = 45
REVIEW_MINUTES = 15
REVIEW_DAY = 3          # Tuesday


def _t(language: str, ar: str, en: str) -> str:
    return ar if language == "ar" else en


def _queues(states: List[learner_state.CourseState]):
    """For each course with work left: the lessons the learner can open next, in order, and
    whether the course stops at a lesson they cannot open yet."""
    out = []
    for state in states:
        queue = []
        locked = False
        for lesson in state.remaining():
            if not state.can_open(lesson):
                locked = True
                break
            queue.append(lesson)
        out.append((state, queue, locked))
    return out


def _sequence(queues, variant: int) -> List[tuple]:
    """The order lessons are studied in. Variant 0 finishes the most active course first;
    an odd variant alternates between the two most active courses."""
    usable = [(state, list(queue)) for state, queue, _ in queues if queue]
    if not usable:
        return []
    if variant % 2 == 0 or len(usable) == 1:
        return [(state, lesson) for state, queue in usable for lesson in queue]
    first, second = usable[0], usable[1]
    merged = []
    for index in range(max(len(first[1]), len(second[1]))):
        for state, queue in (first, second):
            if index < len(queue):
                merged.append((state, queue[index]))
    for state, queue in usable[2:]:
        merged.extend((state, lesson) for lesson in queue)
    return merged


def weekly_plan(db: Session, user_id: int, week_start: date, variant: int, language: str) -> Dict:
    states = learner_state.enrolled_courses(db, user_id, language)
    days = [{"date": (week_start + timedelta(days=offset)).isoformat(), "blocks": []} for offset in range(7)]
    reasons: List[str] = []

    if not states:
        return {
            "status": "no_enrollment", "goal": _t(language, "سجّل في مقرر لتحصل على خطة أسبوعية.",
                                                   "Enroll in a course to get a weekly plan."),
            "totalMinutes": 0, "days": days,
            "reasons": [_t(language, "لا يوجد لديك مقرر مسجّل حالياً، فلا يوجد ما تُبنى عليه الخطة.",
                           "You have no active enrolment yet, so there is nothing to plan from.")],
        }

    queues = _queues(states)
    sequence = _sequence(queues, variant)
    left: Dict[int, int] = {}
    day = 0
    room = DAILY_MINUTES
    for state, lesson in sequence:
        left.setdefault(lesson.id, max(MIN_BLOCK_MINUTES, lesson.estimated_minutes or DEFAULT_LESSON_MINUTES))
        started = False
        while left[lesson.id] > 0 and day < STUDY_DAYS:
            if room < MIN_BLOCK_MINUTES:
                day, room = day + 1, DAILY_MINUTES
                continue
            minutes = min(left[lesson.id], room)
            days[day]["blocks"].append({
                "type": "lesson",
                "title": f"{state.title} · {learner_state.lesson_title(lesson, language)}",
                "minutes": minutes,
                "refId": f"lesson:{lesson.id}",
                "courseId": state.course.slug,
                "lessonId": str(lesson.id),
                "continues": started,
            })
            started = True
            left[lesson.id] -= minutes
            room -= minutes
        if day >= STUDY_DAYS:
            break

    weak = [skill for skill in learner_state.skill_summaries(db, user_id) if skill["status"] == skill_model.NEEDS_REVIEW]
    if weak:
        skill = weak[0]
        days[REVIEW_DAY]["blocks"].append({
            "type": "review",
            "title": _t(language, f"مراجعة: {skill['name']}", f"Review: {skill['name']}"),
            "minutes": REVIEW_MINUTES,
            "refId": "mentor:chat",
        })
        review_reason = (_t(
            language,
            f"{skill['name']} يحتاج مراجعة: {skill['correct']} إجابات صحيحة من {skill['answers']} في أسئلة المرشد.",
            f"{skill['name']} needs review: {skill['correct']} of {skill['answers']} mentor quiz answers were right.",
        ))
    else:
        review_reason = None

    planned = {block.get("courseId") for d in days for block in d["blocks"] if block.get("courseId")}
    for state, queue, locked in queues:
        total = len(state.lessons)
        if not state.remaining():
            continue
        if state.course.slug in planned and queue:
            reasons.append(_t(
                language,
                f"{state.title}: أنهيت {state.done} من {total} دروس؛ التالي «{learner_state.lesson_title(queue[0], language)}».",
                f"{state.title}: {state.done} of {total} lessons completed; next is \"{learner_state.lesson_title(queue[0], language)}\".",
            ))
        if locked:
            reasons.append(_t(
                language,
                f"{state.title}: الدروس التالية تتطلب شراء المقرر، فلم تُضف إلى الخطة.",
                f"{state.title}: the next lessons need the course to be purchased, so they are not in the plan.",
            ))
    if review_reason:
        reasons.append(review_reason)
    reasons.append(_t(
        language,
        f"الخطة تفترض نحو {DAILY_MINUTES} دقيقة يومياً، ستة أيام في الأسبوع، والجمعة للراحة. المدد من تقدير كل درس.",
        f"The plan assumes about {DAILY_MINUTES} minutes a day, six days a week, with Friday free. Durations are each lesson's estimate.",
    ))

    total_minutes = sum(block["minutes"] for d in days for block in d["blocks"])
    primary = next((state for state, queue, _ in queues if queue), None)
    if all(not state.remaining() for state in states):
        status = "all_done"
        goal = _t(language, "أنهيت كل دروس مقرراتك المسجّلة. اختر مقرراً جديداً لتتابع.",
                  "You have finished every lesson of your enrolled courses. Pick a new course to continue.")
    elif primary is None:
        status = "locked"
        goal = _t(language, "الدروس التالية في مقرراتك تتطلب الشراء.", "The next lessons of your courses need a purchase.")
    else:
        status = "ok"
        goal = _t(language, f"تابع {primary.title}", f"Continue {primary.title}")
    return {"status": status, "goal": goal, "totalMinutes": total_minutes, "days": days, "reasons": reasons}
