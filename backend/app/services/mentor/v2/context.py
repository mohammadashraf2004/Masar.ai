"""Server-owned context for Mentor v2.

Only resource ids cross the trust boundary.  Everything that describes the learner --
progress, completed work, skill evidence and recent mistakes -- is loaded for the
authenticated user here.  The ordered ``sources`` list is also the retrieval policy:
current lesson, other lessons of the same course that match the question, current module,
prerequisites, recent mistakes, then general knowledge.

A conversation is about one of three things: a lesson (``lesson:<id>``), a course the learner
is enrolled in and chose in the hub (``course:<slug>`` - its outline and its lessons that match
the question), or nothing (``general`` - general knowledge only, no course material).
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, defer, joinedload

from app.models.learning import Exercise, Lesson, Quiz, Topic
from app.models.learning_path import Course
from app.models.mentor_evidence import MentorEvidence
from app.models.progress import UserProgress
from app.models.tool_course import ToolTopic
from app.services.billing.access_service import (
    active_enrollment, course_access, course_for_content, free_lesson_ids, require_content_access,
    require_lesson_access,
)
from app.services.mentor import learner_state
from app.services.mentor.v2.excerpt import best_passage, plain, terms
from app.services.mentor.v2.skills import RECENT_MISTAKE_DAYS
from app.views.mentor_v2 import MentorContextIn

# What of the learner's own draft reaches the model. The request caps it too.
MAX_LEARNER_CODE_CHARS = 4_000

# Lessons of the conversation's course that match the question. A few open ones (one passage
# each) and a few locked ones (title only), so the mentor can answer from, or point at, any part
# of the course without the current lesson being crowded out.
LIBRARY_OPEN = 3
LIBRARY_LOCKED = 2
LIBRARY_CANDIDATES = 24
LIBRARY_TERMS = 6
LIBRARY_PASSAGE_CHARS = 900
# A course conversation's outline: the course, then its lessons in order.
OUTLINE_CHARS = 3_000
# The hub's course picker: every course a learner is taking, not just the latest few.
ENROLLED_COURSES = 50


@dataclass(frozen=True)
class Source:
    rank: int
    kind: str
    lesson_id: Optional[int]
    title: str
    content: str
    # A lesson later in the module than the current one: the learner has not studied it yet,
    # so the model is told only that it exists (its title), never what it teaches.
    ahead: bool = False
    # The catalogue slug of the course the lesson belongs to, so a reply can point at it.
    course_slug: Optional[str] = None
    # A lesson of the course the learner has not unlocked: its content is only the course name,
    # so the model can point at it but has nothing of the paid text to teach from.
    locked: bool = False


@dataclass(frozen=True)
class QuizItem:
    """An authored question and its key, for the leak check only. Never sent to the model."""
    question: str
    correct: str


@dataclass
class ServerContext:
    lesson: Optional[Lesson] = None
    exercise: Optional[Exercise] = None
    progress: Dict = field(default_factory=dict)
    sources: List[Source] = field(default_factory=list)
    quiz_answers: List[str] = field(default_factory=list)
    quiz_items: List[QuizItem] = field(default_factory=list)
    exercise_solution: Optional[str] = None
    # The learner's selection, when it really is text of the current lesson.
    selected_text: Optional[str] = None
    # A selection that is not in the lesson (pasted, or from elsewhere): passed on as the
    # learner's own words, never attributed to the course.
    learner_quote: Optional[str] = None
    # The exercise as the learner sees it - title, instructions, starter - in their language.
    exercise_view: Optional[Dict] = None
    # What the learner has written in the exercise editor, when they attached it.
    learner_code: Optional[str] = None
    course_slug: Optional[str] = None
    # Set for a course conversation only: the enrolled course the learner chose, with no lesson.
    course: Optional[Course] = None

    @property
    def has_course_context(self) -> bool:
        return self.lesson is not None or self.exercise is not None or self.course is not None

    @property
    def allowed_lesson_ids(self) -> set[int]:
        return {s.lesson_id for s in self.sources if s.lesson_id is not None}

    def source_for(self, lesson_id: int) -> Optional[Source]:
        return next((s for s in self.sources if s.lesson_id == lesson_id), None)


def _lesson_text(lesson: Lesson, language: str) -> tuple[str, str]:
    if language == "ar" and lesson.content_ar:
        return lesson.title_ar or lesson.title, lesson.content_ar
    return lesson.title, lesson.content


def _module(lesson: Lesson):
    return lesson.topic or lesson.tool_topic


def _module_lessons(db: Session, lesson: Lesson) -> List[Lesson]:
    if lesson.topic_id:
        return db.query(Lesson).filter(Lesson.topic_id == lesson.topic_id).order_by(Lesson.order, Lesson.id).all()
    if lesson.tool_topic_id:
        return db.query(Lesson).filter(Lesson.tool_topic_id == lesson.tool_topic_id).order_by(Lesson.order, Lesson.id).all()
    return [lesson]


def _module_lesson_ids(db: Session, lesson: Lesson):
    """The ids of the lesson's module, without reading every lesson's text again."""
    if lesson.topic_id:
        return db.query(Lesson.id).filter(Lesson.topic_id == lesson.topic_id).all()
    if lesson.tool_topic_id:
        return db.query(Lesson.id).filter(Lesson.tool_topic_id == lesson.tool_topic_id).all()
    return [(lesson.id,)]


def _prerequisite_lessons(db: Session, lesson: Lesson) -> List[Lesson]:
    module = _module(lesson)
    ids = [value for value in (getattr(module, "prerequisite_ids", None) or []) if isinstance(value, int)]
    if not ids:
        return []
    if lesson.topic_id:
        return db.query(Lesson).filter(Lesson.topic_id.in_(ids)).order_by(Lesson.topic_id, Lesson.order, Lesson.id).all()
    return db.query(Lesson).filter(Lesson.tool_topic_id.in_(ids)).order_by(Lesson.tool_topic_id, Lesson.order, Lesson.id).all()


def _accessible(db: Session, user_id: int, lessons: List[Lesson]) -> List[Lesson]:
    """`lessons` the learner may read, deciding access once per course.

    The same rule as require_lesson_access (legacy content open; otherwise course access, or
    one of the course's free preview lessons), without re-reading the learner's role, Pro
    status and enrolment for every lesson of the module."""
    courses: Dict[tuple, object] = {}
    allowed: Dict[int, Optional[set]] = {}
    out: List[Lesson] = []
    for item in lessons:
        key = (item.topic_id, item.tool_topic_id)
        if key not in courses:
            courses[key] = course_for_content(db, item)
        course = courses[key]
        if course is None:
            out.append(item)
            continue
        if course.id not in allowed:
            allowed[course.id] = None if course_access(db, user_id, course).has_access else free_lesson_ids(db, course)
        free = allowed[course.id]
        if free is None or item.id in free:
            out.append(item)
    return out


def _progress(db: Session, user_id: int, lesson: Lesson) -> Dict:
    query = db.query(UserProgress).filter(UserProgress.user_id == user_id)
    query = query.filter(
        UserProgress.topic_id == lesson.topic_id if lesson.topic_id else UserProgress.tool_topic_id == lesson.tool_topic_id
    )
    row = query.first()
    if row is None:
        return {"status": "not_started", "lessonsCompleted": [], "exercisesCompleted": []}
    return {
        "status": getattr(row.status, "value", row.status),
        "lessonsCompleted": list(row.lessons_completed or []),
        "exercisesCompleted": list(row.exercises_completed or []),
        "timeSpentMinutes": row.time_spent_minutes or 0,
    }


def _recent_mistakes(db: Session, user_id: int, lesson: Lesson, language: str) -> List[Source]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=RECENT_MISTAKE_DAYS)
    rows = (
        db.query(MentorEvidence)
        .filter(
            MentorEvidence.user_id == user_id,
            MentorEvidence.correct.is_(False),
            MentorEvidence.created_at >= cutoff,
        )
        .order_by(MentorEvidence.created_at.desc(), MentorEvidence.id.desc())
        .limit(8)
        .all()
    )
    out: List[Source] = []
    module_ids = {lesson_id for (lesson_id,) in _module_lesson_ids(db, lesson)}
    quiz_ids = {row.quiz_id for row in rows if row.quiz_id}
    quizzes = {quiz.id: quiz for quiz in db.query(Quiz).filter(Quiz.id.in_(quiz_ids)).all()} if quiz_ids else {}
    for row in rows:
        # Keep mistakes relevant to this module.  Most rows have a lesson id; old/imported
        # questions may not, in which case their quiz must belong to the current module.
        relevant = row.lesson_id in module_ids
        quiz = quizzes.get(row.quiz_id) if row.quiz_id else None
        if not relevant and quiz:
            relevant = quiz.topic_id == lesson.topic_id and quiz.tool_topic_id == lesson.tool_topic_id
        questions = quiz.questions if quiz and isinstance(quiz.questions, list) else []
        if not relevant or row.question_index is None or not 0 <= row.question_index < len(questions):
            continue
        question = questions[row.question_index]
        shown = question
        if language == "ar" and isinstance(quiz.questions_ar, list) and row.question_index < len(quiz.questions_ar):
            shown = quiz.questions_ar[row.question_index]
        prompt = shown.get("question") if isinstance(shown, dict) else None
        options = shown.get("options") if isinstance(shown, dict) else None
        picked = options[row.selected] if isinstance(options, list) and row.selected is not None and 0 <= row.selected < len(options) else None
        if prompt:
            text = f"Mistake: {prompt}" + (f"\nLearner selected: {picked}" if picked else "")
            out.append(Source(4, "mistake", row.lesson_id, row.skill, text))
        if len(out) >= 4:
            break
    return out


def _quiz_items(db: Session, lesson: Lesson) -> List[QuizItem]:
    """Every authored question of the lesson's module with its key, in both languages."""
    query = db.query(Quiz)
    if lesson.topic_id:
        query = query.filter(Quiz.topic_id == lesson.topic_id)
    elif lesson.tool_topic_id:
        query = query.filter(Quiz.tool_topic_id == lesson.tool_topic_id)
    else:
        return []
    items: List[QuizItem] = []
    for quiz in query.all():
        twins = quiz.questions_ar if isinstance(quiz.questions_ar, list) else []
        for index, question in enumerate(quiz.questions if isinstance(quiz.questions, list) else []):
            if not isinstance(question, dict):
                continue
            options, correct = question.get("options"), question.get("correct")
            if not (isinstance(options, list) and isinstance(correct, int) and not isinstance(correct, bool) and 0 <= correct < len(options)):
                continue
            items.append(QuizItem(str(question.get("question") or ""), str(options[correct])))
            twin = twins[index] if index < len(twins) else None
            twin_options = twin.get("options") if isinstance(twin, dict) else None
            if isinstance(twin_options, list) and len(twin_options) == len(options):
                items.append(QuizItem(str(twin.get("question") or ""), str(twin_options[correct])))
    return items


def _quiz_answer_texts(db: Session, lesson: Lesson) -> List[str]:
    return [item.correct for item in _quiz_items(db, lesson)]


def _exercise_view(exercise: Exercise, language: str) -> Dict:
    arabic = language == "ar"
    return {
        "id": str(exercise.id),
        "title": (exercise.title_ar if arabic and exercise.title_ar else exercise.title) or "",
        "instructions": ((exercise.description_ar if arabic and exercise.description_ar else exercise.description) or "")[:1_500],
        "language": exercise.language or "python",
        "starterCode": (exercise.starter_code or "")[:1_500] or None,
    }


def _course_slug(db: Session, lesson: Lesson) -> Optional[str]:
    course = course_for_content(db, lesson)
    if course is not None:
        return course.slug
    if lesson.tool_topic and lesson.tool_topic.tool_course:
        return lesson.tool_topic.tool_course.slug
    if lesson.topic and lesson.topic.level and lesson.topic.level.track:
        return lesson.topic.level.track.slug
    return None


def _course_title(course: Course, language: str) -> str:
    """A catalogue course's name. Imported tool courses keep it on the tool course only."""
    legacy = course.tool_course
    if language == "ar":
        named = course.title_ar or (legacy.title_ar if legacy else None)
        if named:
            return named
    return course.title or (legacy.title if legacy else None) or course.slug


_ARABIC_WORD = re.compile(r"[ء-يٱ-ۓ]")


def _folded(column):
    """Lower-cased, with alef forms made one - the same folding `terms` applies to the question."""
    return func.translate(func.lower(column), "أإآ", "ااا")


def _library(
    db: Session, user_id: int, query: str, language: str, exclude: set[int], courses: List[Course],
) -> List[Source]:
    """Lessons of `courses` (the conversation's course) that match the question, best first.

    Each word of the question counts by how rare it is among those lessons (a word most lessons
    contain, like "work", says little about which lesson is meant), and a title match three
    times a body match. One scan. Only lessons the learner may open are sent with a passage of
    their text; one they have not unlocked is sent as its title and course name only - enough
    to point at, nothing of the paid text."""
    wanted = sorted(terms(query), key=lambda word: (-len(word), word))[:LIBRARY_TERMS]
    if not wanted or not courses:
        return []
    # Only lessons of active catalogue courses: an inactive or test course is not a course.
    by_tool = {course.tool_course_id: course for course in courses if course.tool_course_id}
    by_level = {course.track_level_id: course for course in courses if course.track_level_id}
    in_courses = or_(ToolTopic.tool_course_id.in_(list(by_tool) or [-1]), Topic.level_id.in_(list(by_level) or [-1]))
    arabic = any(_ARABIC_WORD.match(term) for term in wanted)
    # Each text is read and lowered once in the subquery (OFFSET 0 keeps it from being inlined);
    # testing every term with ILIKE against the raw columns read the whole catalogue per term.
    # English words are looked for in the English body, Arabic words in the Arabic one.
    columns = [
        Lesson.id, ToolTopic.tool_course_id, Topic.level_id,
        _folded(Lesson.title + " " + func.coalesce(Lesson.title_ar, "")).label("t"),
        func.lower(func.coalesce(Lesson.content, "")).label("c"),
    ]
    if arabic:
        columns.append(_folded(func.coalesce(Lesson.content_ar, "")).label("ca"))
    texts = (
        db.query(*columns)
        .outerjoin(ToolTopic, Lesson.tool_topic_id == ToolTopic.id)
        .outerjoin(Topic, Lesson.topic_id == Topic.id)
        .filter(in_courses)
        .offset(0)
        .subquery()
    )
    hits = []
    for term in wanted:
        body = texts.c.ca if _ARABIC_WORD.match(term) else texts.c.c
        hits += [func.strpos(texts.c.t, term) > 0, func.strpos(body, term) > 0]
    rows = db.query(texts.c.id, texts.c.tool_course_id, texts.c.level_id, *hits).all()
    found = [sum(1 for row in rows if row[3 + 2 * index] or row[4 + 2 * index]) for index in range(len(wanted))]
    weight = [math.log((len(rows) + 1) / (count + 1)) for count in found]
    scored = []
    for row in rows:
        score = sum(weight[index] * (3 * row[3 + 2 * index] + row[4 + 2 * index]) for index in range(len(wanted)))
        if score > 0 and row[0] not in exclude:
            scored.append((-score, row[0], by_tool.get(row[1]) or by_level.get(row[2])))
    ranked = [(lesson_id, course) for _, lesson_id, course in sorted(scored, key=lambda item: item[:2])[:LIBRARY_CANDIDATES]]
    if not ranked:
        return []
    # Bodies are read only for the few lessons a passage is taken from, not every candidate.
    lessons = {
        row.id: row
        for row in db.query(Lesson).options(defer(Lesson.content), defer(Lesson.content_ar))
        .filter(Lesson.id.in_([lesson_id for lesson_id, _ in ranked])).all()
    }
    readable = {row.id for row in _accessible(db, user_id, list(lessons.values()))}

    out: List[Source] = []
    opened = locked = 0
    for lesson_id, course in ranked:
        lesson = lessons.get(lesson_id)
        if lesson is None:
            continue
        title = lesson.title_ar or lesson.title if language == "ar" else lesson.title
        heading = f"Course: {_course_title(course, language)}"
        if lesson_id in readable and opened < LIBRARY_OPEN:
            title, content = _lesson_text(lesson, language)
            passage = best_passage(content, query=query, budget=LIBRARY_PASSAGE_CHARS)
            out.append(Source(2, "library", lesson.id, title, f"{heading}\n{passage}", course_slug=course.slug))
            opened += 1
        elif lesson_id not in readable and locked < LIBRARY_LOCKED:
            out.append(Source(2, "library", lesson.id, title, heading, course_slug=course.slug, locked=True))
            locked += 1
        if opened >= LIBRARY_OPEN and locked >= LIBRARY_LOCKED:
            break
    return out


def enrolled_course(db: Session, user_id: int, slug: str) -> Course:
    """The active course `slug`, if the learner is enrolled in it: what a course conversation is
    about. Enrolment, not access: a Pro learner still chooses the courses they are taking."""
    course = (
        db.query(Course).options(joinedload(Course.tool_course))
        .filter(Course.slug == slug, Course.is_active.is_(True)).first()
    )
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if active_enrollment(db, user_id, course.id) is None:
        raise HTTPException(status_code=403, detail={"code": "COURSE_NOT_ENROLLED", "course_id": course.slug})
    return course


def _course_outline(state: learner_state.CourseState, course: Course, language: str) -> Source:
    """The course as the learner has it: what it is, then its lessons in order, each marked done
    or locked. Titles only - lesson text comes from the matches for the question."""
    description = (course.description_ar if language == "ar" and course.description_ar else course.description) or ""
    lines = [f"Course: {state.title}"]
    if description:
        lines.append(description.strip()[:600])
    lines.append(f"Lessons ({state.done} of {len(state.lessons)} done):")
    for number, lesson in enumerate(state.lessons, start=1):
        mark = " (done)" if lesson.id in state.completed else "" if state.can_open(lesson) else " (locked)"
        lines.append(f"{number}. {learner_state.lesson_title(lesson, language)}{mark}")
    return Source(1, "course", None, state.title, "\n".join(lines)[:OUTLINE_CHARS], course_slug=course.slug)


def build_context(
    db: Session, user_id: int, supplied: MentorContextIn, language: str = "ar", query: Optional[str] = None,
) -> ServerContext:
    """Resolve ids and retrieve context for *this* user.  No caller-supplied progress exists
    in the schema, and extra fields are ignored by Pydantic before this function runs.

    Every id is checked before anything is read: it must exist (404), the learner must be
    allowed to read it (403), and ids that name more than one thing must agree (422) - an
    exercise must belong to the lesson, the lesson to the course. Nothing is returned for an
    id that fails, so a changed id can never surface someone else's or a locked lesson.

    A `courseId` with no lesson or exercise is a course conversation: the course must be one the
    learner is enrolled in (403 otherwise). `query` (the learner's question) is searched in the
    conversation's course - the chosen one, or the attached lesson's - and nowhere else; with no
    course and no lesson the mentor gets no course material at all."""
    lesson: Optional[Lesson] = None
    exercise: Optional[Exercise] = None
    if supplied.exerciseId:
        exercise = db.query(Exercise).filter(Exercise.id == int(supplied.exerciseId)).first()
        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")
        require_content_access(db, user_id, exercise)
        if exercise.lesson_id:
            lesson = db.query(Lesson).filter(Lesson.id == exercise.lesson_id).first()
    if supplied.lessonId:
        requested = db.query(Lesson).filter(Lesson.id == int(supplied.lessonId)).first()
        if requested is None:
            raise HTTPException(status_code=404, detail="Lesson not found")
        require_lesson_access(db, user_id, requested)
        if lesson is not None and lesson.id != requested.id:
            raise HTTPException(status_code=422, detail="Exercise does not belong to lesson")
        lesson = requested
    elif lesson is not None:
        require_lesson_access(db, user_id, lesson)

    result = ServerContext(lesson=lesson, exercise=exercise)
    if exercise is not None:
        result.exercise_view = _exercise_view(exercise, language)
        result.exercise_solution = exercise.solution_code
        if supplied.attachCode and supplied.code and supplied.code.strip():
            result.learner_code = supplied.code[:MAX_LEARNER_CODE_CHARS]
    if lesson is None:
        # Removing the context chips really means general: do not silently reattach a past
        # lesson or another conversation's mistakes.
        if supplied.selectedText and supplied.selectedText.strip():
            result.learner_quote = supplied.selectedText.strip()
        if supplied.courseId and exercise is None:
            return _course_context(db, user_id, result, supplied.courseId, language, query)
        result.sources.append(Source(5, "general", None, "General knowledge", "No course or lesson was attached."))
        return result

    result.course_slug = _course_slug(db, lesson)
    if supplied.courseId and result.course_slug and supplied.courseId.lower() != result.course_slug.lower():
        raise HTTPException(status_code=422, detail="Lesson does not belong to course")

    result.progress = _progress(db, user_id, lesson)
    current_title, current_content = _lesson_text(lesson, language)
    selected = (supplied.selectedText or "").strip()
    if selected:
        # Compared as rendered text: a selection never contains the markdown (`**`, backticks,
        # link targets) that the stored lesson does.
        if plain(selected) and plain(selected) in plain(current_content):
            result.selected_text = selected
        else:
            result.learner_quote = selected
    # The whole lesson stays here (it is what replies are checked against); message.py sends
    # the model only the part of it that fits and matters.
    slug = result.course_slug
    result.sources.append(Source(1, "current_lesson", lesson.id, current_title, current_content, course_slug=slug))
    module = _module_lessons(db, lesson)
    prerequisites = _prerequisite_lessons(db, lesson)
    course = course_for_content(db, lesson) if query and query.strip() else None
    if course is not None:
        # Matches elsewhere in the course come right after the current lesson: they were found
        # by the question itself, so they outrank neighbours sent only for being nearby.
        nearby = {row.id for row in module} | {row.id for row in prerequisites}
        result.sources.extend(_library(db, user_id, query, language, nearby, [course]))
    for item in _accessible(db, user_id, [row for row in module if row.id != lesson.id]):
        title, content = _lesson_text(item, language)
        ahead = (item.order, item.id) > (lesson.order, lesson.id)
        result.sources.append(Source(2, "current_module", item.id, title, content[:6000], ahead=ahead, course_slug=slug))
    for item in _accessible(db, user_id, prerequisites):
        title, content = _lesson_text(item, language)
        result.sources.append(Source(3, "prerequisite", item.id, title, content[:4000], course_slug=_course_slug(db, item)))
    result.sources.extend(_recent_mistakes(db, user_id, lesson, language))
    result.sources.append(Source(5, "general", None, "General knowledge", "Use only when the course sources do not answer the question."))
    result.quiz_items = _quiz_items(db, lesson)
    result.quiz_answers = [item.correct for item in result.quiz_items]
    return result


def _course_context(
    db: Session, user_id: int, result: ServerContext, slug: str, language: str, query: Optional[str],
) -> ServerContext:
    """A conversation about a whole course the learner is enrolled in: its outline, then its
    lessons that match the question."""
    course = enrolled_course(db, user_id, slug)
    state = learner_state.course_states(db, user_id, [course], language)[0]
    result.course, result.course_slug = course, course.slug
    result.progress = {"lessonsDone": state.done, "lessonsTotal": len(state.lessons)}
    result.sources.append(_course_outline(state, course, language))
    if query and query.strip():
        result.sources.extend(_library(db, user_id, query, language, set(), [course]))
    result.sources.append(Source(5, "general", None, "General knowledge", "Use only when the course sources do not answer the question."))
    return result


def context_reference(
    db: Session,
    user_id: int,
    *,
    lesson_id: Optional[str] = None,
    exercise_id: Optional[str] = None,
    course_id: Optional[str] = None,
    language: str = "ar",
) -> Dict:
    """Return a verified current/selected lesson reference for the Mentor UI.

    Explicit lesson or exercise ids (from a lesson link) win, under the lesson's own access rule.
    A `course_id` (the hub's course picker) must be a course the learner is enrolled in (403
    otherwise) and gives that course's next lesson. With no ids, the enrolled course the learner
    was most recently active in gives its next lesson; with no enrolment there is nothing.
    `courseEnrolled` says whether the reference's course is one the learner is enrolled in -
    only such a course can be the subject of a course conversation. Nothing from a previous
    mentor session is reused, so changing the selected lesson cannot retain stale context.
    """
    exercise = None
    if lesson_id or exercise_id:
        resolved = build_context(db, user_id, MentorContextIn(lessonId=lesson_id, exerciseId=exercise_id), language)
        lesson, exercise = resolved.lesson, resolved.exercise
    else:
        if course_id:
            course = enrolled_course(db, user_id, course_id)
            states = learner_state.course_states(db, user_id, [course], language)
        else:
            states = learner_state.enrolled_courses(db, user_id, language, limit=ENROLLED_COURSES)
        if not states:
            return {}
        state = states[0]
        lesson = learner_state.next_lesson(state)
        if lesson is None:
            return {"courseId": state.course.slug, "courseTitle": state.title, "courseEnrolled": True}
    if lesson is None:
        return {}

    module_lessons = _module_lessons(db, lesson)
    course = course_for_content(db, lesson)
    tool_course = lesson.tool_topic.tool_course if lesson.tool_topic and lesson.tool_topic.tool_course else None
    track = lesson.topic.level.track if lesson.topic and lesson.topic.level and lesson.topic.level.track else None
    if course is not None:
        course_id, shown_course = course.slug, _course_title(course, language)
    else:
        legacy = tool_course or track
        course_id = legacy.slug if legacy else None
        shown_course = None
        if legacy is not None:
            shown_course = legacy.title_ar if language == "ar" and legacy.title_ar else legacy.title
    title, _content = _lesson_text(lesson, language)
    return {
        "courseId": course_id,
        "lessonId": str(lesson.id),
        "exerciseId": str(exercise.id) if exercise else None,
        "courseTitle": shown_course,
        "lessonTitle": title,
        "exerciseTitle": (_exercise_view(exercise, language)["title"] if exercise else None),
        "lessonNumber": next((index + 1 for index, row in enumerate(module_lessons) if row.id == lesson.id), lesson.order),
        "lessonTotal": len(module_lessons),
        "courseEnrolled": course is not None and active_enrollment(db, user_id, course.id) is not None,
    }

