"""
backend/app/services/content/vocabulary_term_service.py

Read-side service for the normalized AI Vocabulary dictionary. Resolving a
term's course/lesson mapping to an actual URL never guesses: it looks up the
real `ToolTopic`/`Lesson` row the curriculum importer wrote (keyed by
`source_key`), and returns no href at all if that row isn't there — a stale
association from an old import is shown as text, never linked to a fabricated
page.
"""
from typing import Dict, List, Optional, Tuple

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.learning import Lesson
from app.models.tool_course import CURRICULUM_CATEGORY, ToolCourse, ToolTopic
from app.models.vocabulary import TermStatus, UserTermProgress
from app.models.vocabulary_term import (
    VocabularyTerm,
    VocabularyTermAssociation,
    VocabularyTermRelation,
)
from app.views.vocabulary_term import (
    CourseMapping,
    LessonMapping,
    RelatedTerm,
    TermProgressState,
    VocabularyTermDetail,
    VocabularyTermSummary,
)

_STATUS_LABEL = {None: "new", TermStatus.encountered: "learning", TermStatus.learned: "mastered"}


def _course_href(course: ToolCourse) -> str:
    if course.category == CURRICULUM_CATEGORY:
        return f"/courses/{course.slug}/learn"
    return f"/tools/{course.slug}"


def _course_for_key(db: Session, course_key: str) -> Optional[ToolCourse]:
    topic = (
        db.query(ToolTopic)
        .filter(ToolTopic.source_key.like(f"{course_key}/%"))
        .first()
    )
    if topic is not None and topic.tool_course is not None:
        return topic.tool_course
    return None


def _courses_for_keys(db: Session, course_keys: List[str]) -> Dict[str, Optional[ToolCourse]]:
    """Batch version of `_course_for_key` — one query for however many course
    keys a term's detail view needs, not one query per key. A term can be
    associated with all 15 courses; resolving each with its own round trip
    does not scale."""
    if not course_keys:
        return {}
    clauses = [ToolTopic.source_key.like(f"{key}/%") for key in course_keys]
    topics = (
        db.query(ToolTopic)
        .options(joinedload(ToolTopic.tool_course))
        .filter(or_(*clauses))
        .all()
    )
    resolved: Dict[str, Optional[ToolCourse]] = {key: None for key in course_keys}
    for topic in topics:
        if topic.tool_course is None or not topic.source_key:
            continue
        for key in course_keys:
            if resolved[key] is None and topic.source_key.startswith(f"{key}/"):
                resolved[key] = topic.tool_course
    return resolved


def _lesson_for_key(db: Session, course_key: str, lesson_key: str) -> Optional[Lesson]:
    return (
        db.query(Lesson)
        .filter(Lesson.source_key == f"{course_key}/{lesson_key}")
        .first()
    )


def _progress_state(status: Optional[TermStatus]) -> TermProgressState:
    return TermProgressState(status=_STATUS_LABEL.get(status, "new"))


def _progress_by_term_id(db: Session, user_id: Optional[int], term_ids: List[int]) -> Dict[int, TermStatus]:
    if not user_id or not term_ids:
        return {}
    rows = (
        db.query(UserTermProgress)
        .filter(
            UserTermProgress.user_id == user_id,
            UserTermProgress.vocabulary_term_id.in_(term_ids),
        )
        .all()
    )
    return {row.vocabulary_term_id: row.status for row in rows}


def list_course_counts(db: Session) -> List[dict]:
    rows = (
        db.query(VocabularyTermAssociation.course_key, func.count(func.distinct(VocabularyTermAssociation.term_id)))
        .join(VocabularyTerm, VocabularyTerm.id == VocabularyTermAssociation.term_id)
        .filter(VocabularyTerm.is_active.is_(True))
        .group_by(VocabularyTermAssociation.course_key)
        .order_by(VocabularyTermAssociation.course_key)
        .all()
    )
    course_keys = [r[0] for r in rows]
    # Batch-resolved so "Browse by Course" (title + count) and matching a
    # learner's enrolled tool-course slug back to its COURSE-XXX key are both
    # one query, not one per course.
    resolved = _courses_for_keys(db, course_keys)
    return [
        {
            "course_key": course_key,
            "term_count": count,
            "course_title": resolved[course_key].title if resolved[course_key] else None,
            "course_slug": resolved[course_key].slug if resolved[course_key] else None,
            "course_href": _course_href(resolved[course_key]) if resolved[course_key] else None,
        }
        for course_key, count in rows
    ]


def list_categories(db: Session) -> List[str]:
    rows = (
        db.query(VocabularyTerm.category)
        .filter(VocabularyTerm.is_active.is_(True), VocabularyTerm.category.isnot(None))
        .distinct()
        .order_by(VocabularyTerm.category)
        .all()
    )
    return [r[0] for r in rows]


def list_category_counts(db: Session) -> List[dict]:
    """One grouped query (not a Python-side scan of every term) — same shape
    as `list_course_counts`, for "Browse by Category"."""
    rows = (
        db.query(VocabularyTerm.category, func.count(VocabularyTerm.id))
        .filter(VocabularyTerm.is_active.is_(True), VocabularyTerm.category.isnot(None))
        .group_by(VocabularyTerm.category)
        .order_by(VocabularyTerm.category)
        .all()
    )
    return [{"category": category, "term_count": count} for category, count in rows]


def list_terms(
    db: Session,
    *,
    user_id: Optional[int],
    search: Optional[str] = None,
    course_key: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    learning_status: Optional[str] = None,
    page: int = 1,
    page_size: int = 24,
) -> Tuple[List[VocabularyTermSummary], int]:
    query = db.query(VocabularyTerm).filter(VocabularyTerm.is_active.is_(True))

    if category:
        query = query.filter(VocabularyTerm.category == category)
    if difficulty:
        query = query.filter(VocabularyTerm.difficulty == difficulty)
    if learning_status in ("learning", "mastered") and user_id:
        status = TermStatus.encountered if learning_status == "learning" else TermStatus.learned
        matching_ids = [
            row[0]
            for row in db.query(UserTermProgress.vocabulary_term_id)
            .filter(UserTermProgress.user_id == user_id, UserTermProgress.status == status)
            .all()
        ]
        query = query.filter(VocabularyTerm.id.in_(matching_ids or [-1]))
    elif learning_status == "new" and user_id:
        seen_ids = [
            row[0]
            for row in db.query(UserTermProgress.vocabulary_term_id)
            .filter(UserTermProgress.user_id == user_id, UserTermProgress.vocabulary_term_id.isnot(None))
            .all()
        ]
        if seen_ids:
            query = query.filter(~VocabularyTerm.id.in_(seen_ids))
    if course_key:
        # An EXISTS subquery, not a join+DISTINCT: `aliases`/`tags` are JSON
        # columns, and Postgres has no equality operator for JSON, so a plain
        # SELECT DISTINCT across them fails.
        query = query.filter(
            VocabularyTerm.associations.any(VocabularyTermAssociation.course_key == course_key)
        )
    if search:
        like = f"%{search.strip()}%"
        # Aliases (a JSON column) aren't reliably ILIKE-able across dialects —
        # matched in Python below instead, merged into this SQL-filtered page.
        query = query.filter(
            or_(
                VocabularyTerm.term_en.ilike(like),
                VocabularyTerm.term_ar.ilike(like),
                VocabularyTerm.acronym.ilike(like),
                VocabularyTerm.definition_en.ilike(like),
                VocabularyTerm.definition_ar.ilike(like),
            )
        )

    total = query.count()
    rows: List[VocabularyTerm] = (
        query.order_by(VocabularyTerm.term_en)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    # A JSON `aliases` column isn't reliably ILIKE-able across SQLite/Postgres,
    # so alias matching happens here — the same terms have already been
    # filtered down to a page's worth by the SQL above when no search is given.
    if search:
        needle = search.strip().lower()
        all_matches = [
            t
            for t in db.query(VocabularyTerm).filter(VocabularyTerm.is_active.is_(True)).all()
            if any(needle in (a or "").lower() for a in (t.aliases or []))
        ]
        extra_ids = {t.id for t in all_matches} - {r.id for r in rows}
        if extra_ids:
            merged = {r.id: r for r in rows}
            for t in all_matches:
                if t.id in extra_ids:
                    merged[t.id] = t
            rows = sorted(merged.values(), key=lambda t: t.term_en)[: page_size]
            total = query.count() + len(extra_ids)

    term_ids = [t.id for t in rows]
    counts = dict(
        db.query(VocabularyTermAssociation.term_id, func.count(func.distinct(VocabularyTermAssociation.course_key)))
        .filter(VocabularyTermAssociation.term_id.in_(term_ids))
        .group_by(VocabularyTermAssociation.term_id)
        .all()
    ) if term_ids else {}
    progress = _progress_by_term_id(db, user_id, term_ids)

    items = [
        VocabularyTermSummary(
            slug=t.slug,
            term_en=t.term_en,
            term_ar=t.term_ar,
            acronym=t.acronym,
            explanation_simple_ar=t.explanation_simple_ar,
            definition_en=t.definition_en,
            definition_ar=t.definition_ar,
            category=t.category,
            difficulty=t.difficulty,
            course_count=counts.get(t.id, 0),
            progress=_progress_state(progress.get(t.id)),
        )
        for t in rows
    ]
    return items, total


def get_term_detail(db: Session, *, slug: str, user_id: Optional[int]) -> Optional[VocabularyTermDetail]:
    term = (
        db.query(VocabularyTerm)
        .filter(VocabularyTerm.slug == slug, VocabularyTerm.is_active.is_(True))
        .first()
    )
    if term is None:
        return None

    course_keys = sorted(
        {
            row[0]
            for row in db.query(VocabularyTermAssociation.course_key)
            .filter(VocabularyTermAssociation.term_id == term.id)
            .distinct()
            .all()
        }
    )
    # Which of those courses have a real, lesson-level association — a
    # course-only mapping (COURSE-006's outline associations) must never be
    # offered to the learner as a "go to this lesson" action.
    lesson_backed_keys = {
        row[0]
        for row in db.query(VocabularyTermAssociation.course_key)
        .filter(VocabularyTermAssociation.term_id == term.id, VocabularyTermAssociation.lesson_key.isnot(None))
        .distinct()
        .all()
    }
    lookup_keys = list(course_keys)
    if term.first_course_key and term.first_course_key not in lookup_keys:
        lookup_keys.append(term.first_course_key)
    courses_by_key = _courses_for_keys(db, lookup_keys)

    courses: List[CourseMapping] = [
        CourseMapping(
            course_key=course_key,
            course_title=courses_by_key[course_key].title if courses_by_key[course_key] else None,
            course_href=_course_href(courses_by_key[course_key]) if courses_by_key[course_key] else None,
            has_lesson_mapping=course_key in lesson_backed_keys,
        )
        for course_key in course_keys
    ]

    first_introduced: Optional[LessonMapping] = None
    if term.first_course_key and term.first_lesson_key:
        lesson = _lesson_for_key(db, term.first_course_key, term.first_lesson_key)
        first_course = courses_by_key.get(term.first_course_key)
        first_introduced = LessonMapping(
            course_key=term.first_course_key,
            lesson_key=term.first_lesson_key,
            lesson_title=lesson.title if lesson else None,
            href=_course_href(first_course) if first_course else None,
        )

    related_rows = (
        db.query(VocabularyTerm)
        .join(VocabularyTermRelation, VocabularyTermRelation.related_term_id == VocabularyTerm.id)
        .filter(VocabularyTermRelation.term_id == term.id)
        .all()
    )
    related = [RelatedTerm(slug=r.slug, term_en=r.term_en, term_ar=r.term_ar) for r in related_rows]

    progress = _progress_by_term_id(db, user_id, [term.id])

    return VocabularyTermDetail(
        slug=term.slug,
        term_en=term.term_en,
        term_ar=term.term_ar,
        acronym=term.acronym,
        aliases=term.aliases or [],
        category=term.category,
        difficulty=term.difficulty,
        tags=term.tags or [],
        definition_en=term.definition_en,
        definition_ar=term.definition_ar,
        explanation_simple_ar=term.explanation_simple_ar,
        why_it_matters_ar=term.why_it_matters_ar,
        example_ar=term.example_ar,
        related_terms=related,
        courses=courses,
        first_introduced=first_introduced,
        progress=_progress_state(progress.get(term.id)),
    )
