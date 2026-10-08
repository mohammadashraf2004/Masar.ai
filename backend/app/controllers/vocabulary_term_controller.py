"""
backend/app/controllers/vocabulary_term_controller.py

The normalized AI Vocabulary API: `GET /vocabulary` (list, filterable,
paginated), `GET /vocabulary/{slug}` (detail), `GET /vocabulary/categories`,
and `POST /vocabulary/{slug}/progress` (mark learning/mastered — reuses the
same `UserTermProgress` table and upgrade-only rule as `/terminology/progress`,
just addressed by the normalized term instead of the raw dictionary id).

Public read access, same reasoning as `/terminology`: the dictionary is
course content and useful before signing up. Progress writes are
authenticated.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_user, get_optional_user
from app.db.session import get_db
from app.models.user import User
from app.models.vocabulary import TermStatus, UserTermProgress
from app.models.vocabulary_term import VocabularyTerm
from app.services.content import vocabulary_term_service as svc
from app.views.vocabulary_term import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    CategoryCount,
    CourseCount,
    VocabularyCategoriesResponse,
    VocabularyCourseCountsResponse,
    VocabularyListResponse,
    VocabularyTermDetail,
    VocabularyTermProgressRequest,
)

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])

_STATUS_BY_LABEL = {"learning": TermStatus.encountered, "mastered": TermStatus.learned}


@router.get("/categories", response_model=VocabularyCategoriesResponse)
def get_categories(db: Session = Depends(get_db)):
    return VocabularyCategoriesResponse(
        categories=svc.list_categories(db),
        counts=[CategoryCount(**row) for row in svc.list_category_counts(db)],
    )


@router.get("/courses", response_model=VocabularyCourseCountsResponse)
def get_course_counts(db: Session = Depends(get_db)):
    return VocabularyCourseCountsResponse(courses=[CourseCount(**row) for row in svc.list_course_counts(db)])


@router.get("/", response_model=VocabularyListResponse)
def list_terms(
    search: Optional[str] = Query(None, max_length=200),
    course_id: Optional[str] = Query(None, alias="course_id", max_length=20),
    category: Optional[str] = Query(None, max_length=60),
    difficulty: Optional[str] = Query(None, pattern="^(beginner|intermediate|advanced)$"),
    status: Optional[str] = Query(None, pattern="^(new|learning|mastered)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    items, total = svc.list_terms(
        db,
        user_id=current_user.id if current_user else None,
        search=search,
        course_key=course_id,
        category=category,
        difficulty=difficulty,
        learning_status=status,
        page=page,
        page_size=page_size,
    )
    return VocabularyListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{slug}", response_model=VocabularyTermDetail)
def get_term(
    slug: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    term = svc.get_term_detail(db, slug=slug, user_id=current_user.id if current_user else None)
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@router.post("/{slug}/progress", response_model=VocabularyTermDetail)
@limiter.limit("60/minute")
def record_term_progress(
    request: Request,
    slug: str,
    payload: VocabularyTermProgressRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.status not in _STATUS_BY_LABEL:
        raise HTTPException(status_code=400, detail="status must be 'learning' or 'mastered'")

    term = db.query(VocabularyTerm).filter(VocabularyTerm.slug == slug, VocabularyTerm.is_active.is_(True)).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")

    status = _STATUS_BY_LABEL[payload.status]
    now = datetime.utcnow()
    row = (
        db.query(UserTermProgress)
        .filter(UserTermProgress.user_id == current_user.id, UserTermProgress.vocabulary_term_id == term.id)
        .first()
    )
    if row is None:
        db.add(
            UserTermProgress(
                user_id=current_user.id,
                term_id=term.slug,
                vocabulary_term_id=term.id,
                status=status,
                learned_at=now if status == TermStatus.learned else None,
            )
        )
    elif status == TermStatus.learned and row.status != TermStatus.learned:
        # Upgrade-only — the same rule /terminology/progress uses: re-reading a
        # lesson must not demote a term the student already proved.
        row.status = TermStatus.learned
        row.learned_at = now
    db.commit()

    return svc.get_term_detail(db, slug=slug, user_id=current_user.id)
