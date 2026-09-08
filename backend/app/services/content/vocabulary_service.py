"""
app/services/content/vocabulary_service.py

Writing English-terminology progress.

Two callers, one upsert:

  * the terminology API, when the reader meets a term in a lesson or marks
    one from the glossary;
  * answer evaluation, which is the *earned* signal — a term counts as
    learned once the student has answered something about it correctly, not
    merely because a paragraph mentioning it scrolled past.

The status only ever moves forward. Re-reading a lesson that mentions a term
must never demote a term the student has already proven.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Sequence, Set

from sqlalchemy.orm import Session

from app.content import terminology as T
from app.models.vocabulary import TermStatus, UserTermProgress


def record_terms(
    db: Session,
    user_id: int,
    term_ids: Iterable[str],
    status: TermStatus,
    *,
    commit: bool = True,
) -> None:
    """Upsert one row per (user, term), upgrading status but never demoting.

    Ids not in the dictionary are dropped silently — callers that need to
    reject them (the API does) validate before calling.
    """
    wanted = {term_id for term_id in term_ids if term_id in T.TERMS}
    if not wanted:
        return

    now = datetime.utcnow()
    existing = {
        row.term_id: row
        for row in db.query(UserTermProgress)
        .filter(
            UserTermProgress.user_id == user_id,
            UserTermProgress.term_id.in_(wanted),
        )
        .all()
    }

    for term_id in wanted:
        row = existing.get(term_id)
        if row is None:
            db.add(
                UserTermProgress(
                    user_id=user_id,
                    term_id=term_id,
                    status=status,
                    learned_at=now if status == TermStatus.learned else None,
                )
            )
        elif status == TermStatus.learned and row.status != TermStatus.learned:
            row.status = TermStatus.learned
            row.learned_at = now

    if commit:
        db.commit()


def terms_from_content(*texts: str, declared: Sequence[str] | None = None) -> List[str]:
    """The vocabulary a piece of content exercises.

    `declared` is the content's own `technical_terms` when an author set it;
    everything else is detected from the text, so a lesson whose author never
    filled that field still contributes progress.
    """
    found: Set[str] = {term_id for term_id in (declared or []) if term_id in T.TERMS}
    for text in texts:
        found.update(T.terms_in_text(text or ""))
    return sorted(found)


def promote_from_correct_answer(
    db: Session,
    user_id: int,
    *texts: str,
    declared: Sequence[str] | None = None,
    commit: bool = True,
) -> List[str]:
    """Mark the terminology of a correctly-answered exercise or question as
    learned. Returns the ids promoted, mostly so callers can log or test it.

    Best-effort by design: vocabulary bookkeeping must never be the reason a
    student's graded answer fails to save.
    """
    term_ids = terms_from_content(*texts, declared=declared)
    if not term_ids:
        return []
    record_terms(db, user_id, term_ids, TermStatus.learned, commit=commit)
    return term_ids
