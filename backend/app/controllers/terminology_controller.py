"""
backend/app/controllers/terminology_controller.py

The terminology dictionary, a student's vocabulary progress, and the
content-authoring lint.

The dictionary itself is public: it is course content, and the glossary is
useful before signing up. Progress is per-user and authenticated. The lint is
authenticated because it is an authoring tool and it does real work per call.
"""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.content import terminology as T
from app.core.limiter import limiter
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.vocabulary import TermStatus, UserTermProgress
from app.services.content.terminology_lint import lint_content
from app.views.terminology import (
    TerminologyLintRequest,
    TerminologyLintResponse,
    TerminologyResponse,
    VocabularyProgressResponse,
    VocabularyRecordRequest,
)

router = APIRouter(prefix="/terminology", tags=["Terminology"])


@router.get("/", response_model=TerminologyResponse)
def get_dictionary():
    """The whole dictionary. Small (tens of KB), static for the life of a
    deployment, and identical for every user — so it is served whole rather
    than paginated or filtered server-side."""
    return TerminologyResponse(
        version=1,
        terms=list(T.TERMS.values()),
        tech_names=T.TECH_NAMES,
    )


# ─── Vocabulary progress ─────────────────────────────────────────────────


@router.get("/progress", response_model=VocabularyProgressResponse)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(UserTermProgress)
        .filter(UserTermProgress.user_id == current_user.id)
        .all()
    )
    return VocabularyProgressResponse(
        # Every row is at least "encountered": `learned` is a strict subset,
        # so the client can render both bars off one response.
        encountered=[row.term_id for row in rows],
        learned=[row.term_id for row in rows if row.status == TermStatus.learned],
        total_terms=len(T.TERMS),
    )


@router.post("/progress", response_model=VocabularyProgressResponse)
@limiter.limit("60/minute")
def record_progress(
    request: Request,
    payload: VocabularyRecordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Record that terms were met, or proven.

    Ids are validated against the loaded dictionary — `term_id` is not a
    foreign key, so this is the only thing standing between the table and
    arbitrary client-supplied strings.
    """
    unknown = [term_id for term_id in payload.term_ids if term_id not in T.TERMS]
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown terminology ids: {', '.join(sorted(set(unknown))[:5])}",
        )

    status = TermStatus(payload.status)
    now = datetime.utcnow()

    existing = {
        row.term_id: row
        for row in db.query(UserTermProgress)
        .filter(
            UserTermProgress.user_id == current_user.id,
            UserTermProgress.term_id.in_(payload.term_ids),
        )
        .all()
    }

    for term_id in set(payload.term_ids):
        row = existing.get(term_id)
        if row is None:
            db.add(
                UserTermProgress(
                    user_id=current_user.id,
                    term_id=term_id,
                    status=status,
                    learned_at=now if status == TermStatus.learned else None,
                )
            )
        elif status == TermStatus.learned and row.status != TermStatus.learned:
            # Only ever an upgrade: re-reading a lesson must not demote a
            # term the student has already proven.
            row.status = TermStatus.learned
            row.learned_at = now

    db.commit()

    return get_progress(current_user=current_user, db=db)


# ─── Authoring lint ──────────────────────────────────────────────────────


@router.post("/lint", response_model=TerminologyLintResponse)
@limiter.limit("30/minute")
def lint(
    request: Request,
    payload: TerminologyLintRequest,
    current_user: User = Depends(get_current_user),
):
    """Advisory check on a draft lesson: which industry terms it uses, and
    where it used an Arabic gloss without ever showing the English term.

    Never blocks anything — the response is a list of suggestions for the
    author to accept or ignore.
    """
    result = lint_content(payload.text)
    return TerminologyLintResponse(
        warnings=result["warnings"],
        terms_used=result["terms_used"],
    )
