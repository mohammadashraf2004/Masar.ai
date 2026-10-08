"""What a learner without access still sees of a paid course's content.

One definition, used by every endpoint that serializes a course's topics
(/tracks/{slug}, /tracks/topics/{id}, /tool-courses/{slug}, /tool-courses/topics/{id}).
It used to be four hand-kept copies, and one of them fell behind and kept
returning hints for locked exercises (audit finding #8).

Locked exercises, projects and quizzes keep an ALLOW-list of catalogue metadata;
every other field is blanked. A field added to a response model later is therefore
hidden from locked content until someone decides it is safe to show. Lessons keep
their metadata and lose their body (`blocks` are rebuilt from the emptied body).
"""
from __future__ import annotations

from typing import Any, Iterable

_EXERCISE_VISIBLE = frozenset({
    "id", "title", "title_ar", "exercise_type", "language", "difficulty", "skill_tested", "lesson_id",
})
_PROJECT_VISIBLE = frozenset({
    "id", "title", "title_ar", "difficulty", "tech_stack", "estimated_hours",
})
_QUIZ_VISIBLE = frozenset({"id", "title", "title_ar", "passing_score"})
_LESSON_BODY = ("content", "content_ar", "blocks", "blocks_ar")
# Required string fields of the response models: blank, not null.
_REQUIRED_TEXT = frozenset({"description"})


def _blank(key: str, value: Any) -> Any:
    if key in _REQUIRED_TEXT:
        return ""
    if isinstance(value, bool):
        return False
    if isinstance(value, list):
        return []
    if isinstance(value, dict):
        return {}
    return None


def _lock(item: dict, visible: frozenset, course_slug: str) -> None:
    for key in list(item):
        if key not in visible:
            item[key] = _blank(key, item[key])
    item.update(is_locked=True, course_slug=course_slug)


def redact_topic(
    topic: dict, course_slug: str, *, free_lesson_ids: Iterable[int],
    free_exercise_ids: Iterable[int], free_quiz_ids: Iterable[int],
) -> None:
    """Redact one serialized topic in place for a learner without access to its course."""
    free_lessons, free_exercises, free_quizzes = set(free_lesson_ids), set(free_exercise_ids), set(free_quiz_ids)
    for lesson in topic.get("lessons", []):
        if lesson["id"] in free_lessons:
            lesson["is_preview"] = True
            continue
        for key in _LESSON_BODY:
            if key in lesson:
                lesson[key] = "" if key == "content" else None
        lesson.update(is_locked=True, course_slug=course_slug)
    for exercise in topic.get("exercises", []):
        if exercise["id"] not in free_exercises:
            _lock(exercise, _EXERCISE_VISIBLE, course_slug)
    for project in topic.get("projects", []):  # projects have no free preview
        _lock(project, _PROJECT_VISIBLE, course_slug)
    for quiz in topic.get("quizzes", []):
        if quiz["id"] not in free_quizzes:
            _lock(quiz, _QUIZ_VISIBLE, course_slug)
