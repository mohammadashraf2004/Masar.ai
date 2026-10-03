"""Server-side context for Mentor v2.

Everything the mentor knows about the learner is read here, from the
database, keyed by the authenticated user. The request contributes only
which lesson/exercise is open and what the learner asked, never what they
have completed, mastered or scored.

Retrieval order, which is also the order the prompt lists it in:
    1. current lesson
    2. current module (the other lessons of the same topic)
    3. prerequisite lessons (the topic's prerequisite_ids)
    4. the learner's recent mistakes
    5. general knowledge (no retrieval; the model's own)
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.learning import CareerTrack, Exercise, Lesson, Quiz, Topic, TrackLevel
from app.models.progress import MentorQuizAnswer, UserProgress, UserSkillScore
from app.models.tool_course import ToolCourse, ToolTopic
from app.services.mentor.mentor_text import overlap, split_chunks, token_set, tokens

TIER_LIMITS = {"lesson": 4, "module": 3, "prerequisite": 2}
MAX_MISTAKES = 5
MAX_PREREQ_TOPICS = 3


@dataclass
class Chunk:
    tier: str
    text: str
    lesson_id: int
    lesson_title: str


@dataclass
class QuizKey:
    """A quiz question and its correct option, kept server-side so the
    validator can tell when a reply gives the answer away."""
    question: str
    correct_text: str


@dataclass
class MentorContext:
    language: str
    lesson: Optional[Lesson] = None
    lesson_title: Optional[str] = None
    exercise: Optional[Exercise] = None
    exercise_title: Optional[str] = None
    module_title: Optional[str] = None
    # Lesson order -> title for every lesson in the module, so the
    # validator can reject "as we saw in lesson 12" when there is no 12.
    module_lessons: Dict[int, str] = field(default_factory=dict)
    chunks: List[Chunk] = field(default_factory=list)
    mistakes: List[str] = field(default_factory=list)
    lessons_completed: int = 0
    lesson_completed: bool = False
    skills: List[Tuple[str, float]] = field(default_factory=list)
    quiz_keys: List[QuizKey] = field(default_factory=list)
    quizzes: List[Quiz] = field(default_factory=list)
    solution_code: Optional[str] = None

    @property
    def has_course_context(self) -> bool:
        return self.lesson is not None or self.exercise is not None

    def tiers(self) -> List[str]:
        present = {c.tier for c in self.chunks}
        if self.mistakes:
            present.add("mistakes")
        return [t for t in ("lesson", "module", "prerequisite", "mistakes") if t in present]

    def chunks_for(self, tier: str) -> List[Chunk]:
        return [c for c in self.chunks if c.tier == tier]


def _pick(lang: str, en: Optional[str], ar: Optional[str]) -> str:
    return (ar or en or "") if lang == "ar" else (en or ar or "")


def _topic_of(db: Session, obj) -> Tuple[Optional[object], str]:
    """The (available) topic a lesson/exercise/quiz belongs to: a track
    Topic under an active track, or a ToolTopic under an active course.
    Returns (None, kind) when its parent is retired or unpublished, the
    same "not found" rule GET /tracks/topics/{id} applies."""
    if getattr(obj, "topic_id", None):
        topic = (
            db.query(Topic)
            .join(TrackLevel, Topic.level_id == TrackLevel.id)
            .join(CareerTrack, TrackLevel.track_id == CareerTrack.id)
            .filter(Topic.id == obj.topic_id, CareerTrack.is_active == True)  # noqa: E712
            .first()
        )
        return topic, "track"
    if getattr(obj, "tool_topic_id", None):
        topic = (
            db.query(ToolTopic)
            .join(ToolCourse, ToolTopic.tool_course_id == ToolCourse.id)
            .filter(ToolTopic.id == obj.tool_topic_id, ToolCourse.is_active == True)  # noqa: E712
            .first()
        )
        return topic, "tool"
    return None, ""


def load_available_quiz(db: Session, quiz_id: int) -> Tuple[Quiz, object]:
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    topic = _topic_of(db, quiz)[0] if quiz else None
    if not quiz or topic is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz, topic


def quiz_questions(quiz: Quiz, lang: str) -> List[dict]:
    """The question list in the reader's language. The Arabic blob is used
    only when it lines up 1:1 with the English one, so an index always
    means the same question whichever language it was read in."""
    en = quiz.questions if isinstance(quiz.questions, list) else []
    ar = quiz.questions_ar if isinstance(quiz.questions_ar, list) else None
    if lang == "ar" and ar and len(ar) == len(en):
        return ar
    return en


def is_gradable(q) -> bool:
    return (
        isinstance(q, dict)
        and q.get("type", "mcq") != "open"
        and isinstance(q.get("options"), list)
        and len(q["options"]) >= 2
        and isinstance(q.get("correct"), int)
        and 0 <= q["correct"] < len(q["options"])
    )


def _rank(chunks: List[Chunk], query_tokens: set, limit: int, pad: bool = False) -> List[Chunk]:
    """Best matches for the question first. With `pad`, the rest of the
    slots are filled in document order: the current lesson is always in
    context, even for "hint please" or "quiz me", which match nothing."""
    scored = [(overlap(tokens(c.text), query_tokens), i, c) for i, c in enumerate(chunks)] if query_tokens else []
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda s: (-s[0], s[1]))
    picked = [c for _, _, c in scored[:limit]]
    if pad or not query_tokens:
        picked += [c for c in chunks if c not in picked][: limit - len(picked)]
    return picked


def _lesson_chunks(lesson: Lesson, tier: str, lang: str) -> List[Chunk]:
    title = _pick(lang, lesson.title, lesson.title_ar)
    body = _pick(lang, lesson.content, lesson.content_ar)
    return [Chunk(tier, t, lesson.id, title) for t in split_chunks(body)]


def build_context(
    db: Session,
    user_id: int,
    *,
    lesson_id: Optional[int],
    exercise_id: Optional[int],
    query: str,
    language: str,
) -> MentorContext:
    ctx = MentorContext(language=language)
    topic = None

    if lesson_id is not None:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        topic = _topic_of(db, lesson)[0] if lesson else None
        if not lesson or topic is None:
            raise HTTPException(status_code=404, detail="Lesson not found")
        ctx.lesson = lesson
        ctx.lesson_title = _pick(language, lesson.title, lesson.title_ar)

    if exercise_id is not None:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        ex_topic = _topic_of(db, exercise)[0] if exercise else None
        if not exercise or ex_topic is None:
            raise HTTPException(status_code=404, detail="Exercise not found")
        if topic is not None and (type(ex_topic), ex_topic.id) != (type(topic), topic.id):
            # An exercise from another module would quietly mix two
            # unrelated contexts; refuse rather than guess which one counts.
            raise HTTPException(status_code=422, detail="Exercise does not belong to this lesson's module")
        topic = topic or ex_topic
        ctx.exercise = exercise
        ctx.exercise_title = _pick(language, exercise.title, exercise.title_ar)
        ctx.solution_code = exercise.solution_code

    if topic is None:
        # No course context attached: no retrieval and no learner state.
        # The learner detached it on purpose, so the answer is "general".
        return ctx

    ctx.module_title = _pick(language, topic.title, topic.title_ar)
    q = token_set(query)

    siblings = list(topic.lessons or [])
    ctx.module_lessons = {l.order: _pick(language, l.title, l.title_ar) for l in siblings}

    if ctx.lesson is not None:
        ctx.chunks += _rank(_lesson_chunks(ctx.lesson, "lesson", language), q, TIER_LIMITS["lesson"], pad=True)
    if ctx.exercise is not None:
        desc = _pick(language, ctx.exercise.description, ctx.exercise.description_ar)
        ctx.chunks.insert(0, Chunk("lesson", desc[:700], ctx.lesson.id if ctx.lesson else 0,
                                   ctx.exercise_title or ""))

    module_chunks: List[Chunk] = []
    for l in siblings:
        if ctx.lesson is not None and l.id == ctx.lesson.id:
            continue
        module_chunks += _lesson_chunks(l, "module", language)
    ctx.chunks += _rank(module_chunks, q, TIER_LIMITS["module"])

    prereq_ids = [i for i in (topic.prerequisite_ids or []) if isinstance(i, int)][:MAX_PREREQ_TOPICS]
    if prereq_ids:
        model = type(topic)
        prereq_chunks: List[Chunk] = []
        for p in db.query(model).filter(model.id.in_(prereq_ids)).all():
            for l in (p.lessons or []):
                prereq_chunks += _lesson_chunks(l, "prerequisite", language)
        ctx.chunks += _rank(prereq_chunks, q, TIER_LIMITS["prerequisite"])

    # ── The learner's own state. Every query below is scoped to user_id,
    #    the authenticated caller; nothing in the request can widen it.
    progress_q = db.query(UserProgress).filter(UserProgress.user_id == user_id)
    if isinstance(topic, Topic):
        progress = progress_q.filter(UserProgress.topic_id == topic.id).first()
    else:
        progress = progress_q.filter(UserProgress.tool_topic_id == topic.id).first()
    completed = list((progress.lessons_completed if progress else None) or [])
    ctx.lessons_completed = len(completed)
    ctx.lesson_completed = bool(ctx.lesson and ctx.lesson.id in completed)

    mistakes = (
        db.query(MentorQuizAnswer)
        .filter(MentorQuizAnswer.user_id == user_id, MentorQuizAnswer.is_correct == False)  # noqa: E712
        .order_by(MentorQuizAnswer.created_at.desc(), MentorQuizAnswer.id.desc())
        .limit(MAX_MISTAKES)
        .all()
    )
    ctx.mistakes = [f"{m.skill_name}: {m.question_text or ''}".strip() for m in mistakes]

    ctx.skills = [
        (s.skill_name, round((s.score or 0) / 100, 2))
        for s in db.query(UserSkillScore).filter(UserSkillScore.user_id == user_id).limit(12).all()
    ]

    ctx.quizzes = list(topic.quizzes or [])
    for quiz in ctx.quizzes:
        # Both languages: a leak in either is a leak.
        for blob in (quiz.questions, quiz.questions_ar):
            for qq in (blob if isinstance(blob, list) else []):
                if is_gradable(qq):
                    ctx.quiz_keys.append(QuizKey(str(qq.get("question", "")), str(qq["options"][qq["correct"]])))
    return ctx
