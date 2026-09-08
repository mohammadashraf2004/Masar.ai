"""
backend/app/controllers/search_controller.py

Bilingual course search.

The requirement it exists to satisfy: "Embeddings", "embedding" and
"التضمينات" must find the same lesson. The platform holds one course per
subject, authored Arabic-first with English terminology preserved — not an
Arabic catalogue beside an English one — so search has to bridge the two
languages instead of the content being duplicated.

How: the query is expanded through the terminology dictionary into every way
its terms can be written (English, Arabic, abbreviation, aliases), and each
of those is matched against both the English and the Arabic columns. Ranking
happens in Python over a bounded candidate set — the corpus is a few hundred
rows, and this keeps the SQL portable rather than tying search to Postgres
full-text configuration that has no Arabic dictionary installed anyway.
"""
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.content import terminology as T
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.learning import CareerTrack, Lesson, Topic, TrackLevel
from app.models.tool_course import ToolCourse, ToolTopic
from app.views.terminology import SearchHit, SearchResponse

router = APIRouter(prefix="/search", tags=["Search"])

# Weights per field. A title hit is what the user almost always means; a body
# hit is a fallback that should never outrank one.
_TITLE_WEIGHT = 10.0
_DESCRIPTION_WEIGHT = 4.0
_BODY_WEIGHT = 1.5

# Bounds on the work one query can cause. The corpus is small; these exist so
# a pathological query ("a") cannot pull every lesson body into memory.
_MAX_SURFACES = 12
_CANDIDATES_PER_KIND = 60
_MAX_HITS = 30


def _like_clauses(columns, surfaces: List[str]):
    """OR of `column ILIKE '%surface%'` across every column and surface."""
    clauses = []
    for surface in surfaces:
        pattern = f"%{surface}%"
        for column in columns:
            clauses.append(column.ilike(pattern))
    return clauses


def _score(surfaces: List[str], fields: List[Tuple[Optional[str], float]]) -> float:
    """Sum the weights of the fields that contain any expanded surface form.

    Case-insensitive on the Latin side; Arabic has no case, so a plain
    substring test is correct there.
    """
    total = 0.0
    for value, weight in fields:
        if not value:
            continue
        haystack = value.lower()
        if any(surface.lower() in haystack for surface in surfaces):
            total += weight
    return total


@router.get("/", response_model=SearchResponse)
@limiter.limit("30/minute")
def search(
    request: Request,
    q: str = Query(..., min_length=2, max_length=120),
    db: Session = Depends(get_db),
):
    surfaces = T.expand_query_surfaces(q)[:_MAX_SURFACES]
    matched_term_ids = T.terms_in_query(q)

    if not surfaces:
        return SearchResponse(query=q, expanded=[], matched_terms=[], hits=[])

    hits: List[SearchHit] = []

    # ── Tool courses ─────────────────────────────────────────────────────
    courses = (
        db.query(ToolCourse)
        .filter(ToolCourse.is_active == True)  # noqa: E712 — SQLAlchemy needs ==
        .filter(
            or_(
                *_like_clauses(
                    [
                        ToolCourse.title,
                        ToolCourse.title_ar,
                        ToolCourse.description,
                        ToolCourse.description_ar,
                    ],
                    surfaces,
                )
            )
        )
        .limit(_CANDIDATES_PER_KIND)
        .all()
    )
    for course in courses:
        hits.append(
            SearchHit(
                kind="tool_course",
                id=course.id,
                title=course.title,
                title_ar=course.title_ar,
                description=course.description,
                description_ar=course.description_ar,
                href=f"/tools/{course.slug}",
                parent_title=course.category,
                score=_score(
                    surfaces,
                    [
                        (course.title, _TITLE_WEIGHT),
                        (course.title_ar, _TITLE_WEIGHT),
                        (course.description, _DESCRIPTION_WEIGHT),
                        (course.description_ar, _DESCRIPTION_WEIGHT),
                    ],
                ),
                matched_terms=list(course.technical_terms or []),
            )
        )

    # ── Tool topics ──────────────────────────────────────────────────────
    topics = (
        db.query(ToolTopic)
        .options(joinedload(ToolTopic.tool_course))
        .filter(
            or_(
                *_like_clauses(
                    [
                        ToolTopic.title,
                        ToolTopic.title_ar,
                        ToolTopic.description,
                        ToolTopic.description_ar,
                    ],
                    surfaces,
                )
            )
        )
        .limit(_CANDIDATES_PER_KIND)
        .all()
    )
    for topic in topics:
        course = topic.tool_course
        if course is None or not course.is_active:
            continue
        hits.append(
            SearchHit(
                kind="tool_topic",
                id=topic.id,
                title=topic.title,
                title_ar=topic.title_ar,
                description=topic.description,
                description_ar=topic.description_ar,
                href=f"/tools/{course.slug}",
                parent_title=course.title,
                score=_score(
                    surfaces,
                    [
                        (topic.title, _TITLE_WEIGHT),
                        (topic.title_ar, _TITLE_WEIGHT),
                        (topic.description, _DESCRIPTION_WEIGHT),
                        (topic.description_ar, _DESCRIPTION_WEIGHT),
                    ],
                ),
                matched_terms=list(topic.technical_terms or []),
            )
        )

    # ── Career tracks ────────────────────────────────────────────────────
    tracks = (
        db.query(CareerTrack)
        .filter(CareerTrack.is_active == True)  # noqa: E712
        .filter(
            or_(
                *_like_clauses(
                    [
                        CareerTrack.title,
                        CareerTrack.title_ar,
                        CareerTrack.description,
                        CareerTrack.description_ar,
                    ],
                    surfaces,
                )
            )
        )
        .limit(_CANDIDATES_PER_KIND)
        .all()
    )
    for track in tracks:
        hits.append(
            SearchHit(
                kind="track",
                id=track.id,
                title=track.title,
                title_ar=track.title_ar,
                description=track.description,
                description_ar=track.description_ar,
                href=f"/tracks/{track.slug}",
                score=_score(
                    surfaces,
                    [
                        (track.title, _TITLE_WEIGHT),
                        (track.title_ar, _TITLE_WEIGHT),
                        (track.description, _DESCRIPTION_WEIGHT),
                        (track.description_ar, _DESCRIPTION_WEIGHT),
                    ],
                ),
            )
        )

    # ── Track topics ─────────────────────────────────────────────────────
    track_topics = (
        db.query(Topic)
        .options(joinedload(Topic.level).joinedload(TrackLevel.track))
        .filter(
            or_(
                *_like_clauses(
                    [Topic.title, Topic.title_ar, Topic.description, Topic.description_ar],
                    surfaces,
                )
            )
        )
        .limit(_CANDIDATES_PER_KIND)
        .all()
    )
    for topic in track_topics:
        track = topic.level.track if topic.level else None
        if track is None:
            continue
        hits.append(
            SearchHit(
                kind="topic",
                id=topic.id,
                title=topic.title,
                title_ar=topic.title_ar,
                description=topic.description,
                description_ar=topic.description_ar,
                href=f"/tracks/{track.slug}",
                parent_title=track.title,
                score=_score(
                    surfaces,
                    [
                        (topic.title, _TITLE_WEIGHT),
                        (topic.title_ar, _TITLE_WEIGHT),
                        (topic.description, _DESCRIPTION_WEIGHT),
                        (topic.description_ar, _DESCRIPTION_WEIGHT),
                    ],
                ),
                matched_terms=list(topic.technical_terms or []),
            )
        )

    # ── Lessons ──────────────────────────────────────────────────────────
    # Titles and bodies, both languages. A body hit is worth little, but it
    # is what makes "reranking" find the lesson that teaches it under a
    # different title.
    lessons = (
        db.query(Lesson)
        .options(
            joinedload(Lesson.tool_topic).joinedload(ToolTopic.tool_course),
            joinedload(Lesson.topic).joinedload(Topic.level).joinedload(TrackLevel.track),
        )
        .filter(
            or_(
                *_like_clauses(
                    [Lesson.title, Lesson.title_ar, Lesson.content, Lesson.content_ar],
                    surfaces,
                )
            )
        )
        .limit(_CANDIDATES_PER_KIND)
        .all()
    )
    for lesson in lessons:
        href: Optional[str] = None
        parent: Optional[str] = None
        if lesson.tool_topic is not None and lesson.tool_topic.tool_course is not None:
            href = f"/tools/{lesson.tool_topic.tool_course.slug}"
            parent = lesson.tool_topic.title
        elif lesson.topic is not None and lesson.topic.level is not None:
            track = lesson.topic.level.track
            if track is not None:
                href = f"/tracks/{track.slug}"
                parent = lesson.topic.title
        if href is None:
            continue

        hits.append(
            SearchHit(
                kind="lesson",
                id=lesson.id,
                title=lesson.title,
                title_ar=lesson.title_ar,
                href=href,
                parent_title=parent,
                score=_score(
                    surfaces,
                    [
                        (lesson.title, _TITLE_WEIGHT),
                        (lesson.title_ar, _TITLE_WEIGHT),
                        (lesson.content, _BODY_WEIGHT),
                        (lesson.content_ar, _BODY_WEIGHT),
                    ],
                ),
            )
        )

    hits.sort(key=lambda hit: (-hit.score, hit.kind, hit.title))

    return SearchResponse(
        query=q,
        expanded=sorted(T.expand_query(q)),
        matched_terms=[T.TERMS[term_id] for term_id in matched_term_ids],
        hits=hits[:_MAX_HITS],
    )
