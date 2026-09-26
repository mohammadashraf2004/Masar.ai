"""
app/services/learning/readiness_assessment.py

The short "am I ready?" check a learner can take before a course.

It reuses the quiz architecture instead of inventing a second one: the questions
are the multiple-choice questions already authored in the quizzes of the
course's *prerequisite* courses (`quizzes.questions`), so nothing is generated
and the check measures exactly what the course assumes.

Trust boundaries
----------------
* Which questions are asked is decided here, deterministically, from the
  catalogue. The client never names questions to be graded, so it cannot pick
  easy ones.
* The answer key never leaves the server: the question list carries no `correct`
  value and no explanation. Grading recomputes the same list and compares the
  submitted option indices against it.
* The score, the per-skill results and the resulting readiness are computed and
  stored here. A request field called `score` or `readiness` does not exist.
* Answers that name a question outside the check, or an option outside its
  options, are rejected rather than ignored.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sqlalchemy.orm import Session

from app.models.learning import Quiz, Topic
from app.models.learning_path import COURSE_KIND_TOOL, Course, ReadinessAssessment
from app.models.tool_course import ToolTopic
from app.models.user import User
from app.services.learning.catalog_service import CatalogBundle
from app.services.learning.readiness import requirements_for

MAX_QUESTIONS = 10
MIN_QUESTIONS = 3          # below this a "check" would be a coin flip; report it unavailable instead
PER_SKILL = 2


@dataclass(frozen=True)
class AssessmentQuestion:
    id: str                          # "<quiz id>:<index>"
    skill: str
    question: str
    options: Tuple[str, ...]
    question_ar: Optional[str]
    options_ar: Optional[Tuple[str, ...]]
    # Private: never serialised to a client before grading.
    correct: int = field(repr=False, default=-1)
    explanation: str = field(repr=False, default="")


class AssessmentInvalid(ValueError):
    """The submission names something the check did not ask."""

    def __init__(self, code: str, detail: str):
        self.code, self.detail = code, detail
        super().__init__(detail)


def _mcq(raw: Any) -> bool:
    return (
        isinstance(raw, dict) and isinstance(raw.get("options"), list) and len(raw["options"]) >= 2
        and isinstance(raw.get("correct"), int) and not isinstance(raw["correct"], bool)
        and 0 <= raw["correct"] < len(raw["options"]) and isinstance(raw.get("question"), str)
        and raw.get("type", "mcq") != "open"
    )


def _pool(db: Session, bundle: CatalogBundle, course_ids: Sequence[int]) -> List[Tuple[int, int, Any, Any]]:
    """`(quiz id, question index, question, its Arabic twin)` for every
    multiple-choice question in the given courses, in a stable order."""
    pool: List[Tuple[int, int, Any, Any]] = []
    for cid in sorted(course_ids):
        course = bundle.courses.get(cid)
        if course is None:
            continue
        if course.kind == COURSE_KIND_TOOL:
            query = (db.query(Quiz).join(ToolTopic, Quiz.tool_topic_id == ToolTopic.id)
                     .filter(ToolTopic.tool_course_id == course.tool_course_id).order_by(ToolTopic.order, Quiz.id))
        else:
            query = (db.query(Quiz).join(Topic, Quiz.topic_id == Topic.id)
                     .filter(Topic.level_id == course.track_level_id).order_by(Topic.order, Quiz.id))
        for quiz in query.all():
            twin = quiz.questions_ar if isinstance(quiz.questions_ar, list) else None
            for index, raw in enumerate(quiz.questions if isinstance(quiz.questions, list) else []):
                if _mcq(raw):
                    pool.append((quiz.id, index, raw, twin[index] if twin and index < len(twin) else None))
    return pool


def select_questions(db: Session, bundle: CatalogBundle, course: Course) -> List[AssessmentQuestion]:
    """The check for `course`: up to `MAX_QUESTIONS` questions, spread over the
    skills its prerequisites teach (required skills first) and over the lessons
    that teach them. Deterministic, so the list a learner is shown is the list
    that is graded."""
    info = bundle.catalog.courses.get(course.id)
    if info is None:
        return []
    requirements = sorted(requirements_for(bundle.catalog, info), key=lambda r: (not r.required, r.skill))
    if not requirements:
        return []
    per_skill = max(1, min(PER_SKILL, MAX_QUESTIONS // len(requirements)))

    chosen: List[AssessmentQuestion] = []
    used: set = set()
    for req in requirements:
        if len(chosen) >= MAX_QUESTIONS:
            break
        providers = [c for c in req.courses if c in bundle.catalog.courses and bundle.catalog.courses[c].is_available]
        pool = _pool(db, bundle, providers)
        if not pool:
            continue
        taken = 0
        for k in range(len(pool)):
            if taken >= per_skill or len(chosen) >= MAX_QUESTIONS:
                break
            # Evenly spaced through the pool, so one skill's questions come from different lessons.
            position = (int((taken + 0.5) * len(pool) / per_skill) + k) % len(pool)
            quiz_id, index, raw, twin = pool[position]
            qid = f"{quiz_id}:{index}"
            if qid in used:
                continue
            used.add(qid)
            taken += 1
            chosen.append(AssessmentQuestion(
                id=qid, skill=req.skill, question=raw["question"], options=tuple(raw["options"]),
                question_ar=twin.get("question") if isinstance(twin, dict) else None,
                options_ar=tuple(twin["options"]) if isinstance(twin, dict) and isinstance(twin.get("options"), list) else None,
                correct=raw["correct"], explanation=str(raw.get("explanation") or ""),
            ))
    return chosen if len(chosen) >= MIN_QUESTIONS else []


def estimated_minutes(count: int) -> int:
    return max(1, math.ceil(count * 0.75))


@dataclass
class QuestionResult:
    id: str
    correct: bool
    explanation: str


@dataclass
class AssessmentOutcome:
    assessment_id: int
    score: float
    correct_count: int
    question_count: int
    skill_results: Dict[str, float]
    questions: List[QuestionResult] = field(default_factory=list)


def grade(
    db: Session, bundle: CatalogBundle, user: User, course: Course, answers: Dict[str, int],
) -> AssessmentOutcome:
    """Score a submission against the server's own copy of the check and store it.
    Unanswered questions count as wrong. Commits."""
    questions = select_questions(db, bundle, course)
    if not questions:
        raise AssessmentInvalid("assessment_unavailable", "This course has no readiness check.")
    by_id = {q.id: q for q in questions}
    for qid, choice in answers.items():
        question = by_id.get(qid)
        if question is None:
            raise AssessmentInvalid("unknown_question", f"'{qid}' is not a question of this check.")
        if isinstance(choice, bool) or not isinstance(choice, int) or not 0 <= choice < len(question.options):
            raise AssessmentInvalid("invalid_answer", f"Answer to '{qid}' is not one of its options.")

    per_skill: Dict[str, List[bool]] = {}
    results: List[QuestionResult] = []
    for q in questions:
        right = answers.get(q.id) == q.correct
        per_skill.setdefault(q.skill, []).append(right)
        results.append(QuestionResult(q.id, right, q.explanation))
    correct = sum(1 for r in results if r.correct)
    skill_results = {skill: sum(v) / len(v) for skill, v in per_skill.items()}
    score = round(100.0 * correct / len(questions), 1)

    row = ReadinessAssessment(
        user_id=user.id, course_id=course.id, question_count=len(questions), correct_count=correct,
        score=score, skill_results=skill_results, answers={k: int(v) for k, v in answers.items()},
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return AssessmentOutcome(row.id, score, correct, len(questions), skill_results, results)
