"""
A mentor quiz question in the learner's UI language.

Authored questions are written in one language. When the learner reads Masar in the other one,
the question is translated here, once, and kept (`MentorQuizTranslation`), so the cost is one
provider call per question per language, and a free quiz stays free for the learner.

This module only ever produces *display* text. It never sees the answer key, and a
translation is accepted only when it lines up with the authored question one to one: the same
number of options in the same order, no two options collapsed into one, and every piece of
code or identifier the author wrote still present. Anything else, or any provider failure,
returns the authored text, so a quiz never fails because a translation did.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.learning import Quiz
from app.models.mentor_translation import MentorQuizTranslation
from app.services import get_llm
from app.services.curriculum.normalize import is_arabic
from app.services.language.arabic_review import TECHNICAL
from app.services.utils import parse_json_response, require_text

logger = logging.getLogger(__name__)

LANGUAGES = ("ar", "en")
# A question the model could not translate acceptably (or a provider error) is
# remembered for this long, so a learner - or a script - reloading it does not
# buy two provider calls per request (audit finding #6).
FAILURE_RETRY_AFTER = timedelta(hours=6)
_FAILED = "__failed_at__"
_NAMES = {"ar": "Arabic", "en": "English"}

SYSTEM = """You translate one multiple-choice course question for a learner.
Return JSON only: {"question": string, "options": [string, ...], "explanation": string}.
Translate into {target}. Keep exactly the same number of options, in the same order, and keep
every option distinct. Do not answer, hint at, reorder or reveal anything about the question.
Never translate or change code, identifiers, function or class names, file names, commands,
numbers, units or technical terms that are normally left in English; copy them exactly as
written. If the explanation is empty, return an empty string for it."""

# What an author writes that must survive a translation untouched: one definition, shared with the
# course-Arabic checks (`inline code`, snake_case, camelCase, ALL_CAPS, calls like fit(), dotted names).
_TECHNICAL = TECHNICAL


def text_language(question: Dict[str, Any]) -> str:
    """The language a question is written in, judged by its script."""
    body = " ".join([str(question.get("question") or "")] + [str(o) for o in question.get("options") or []])
    return "ar" if is_arabic(body) else "en"


def _source(question: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "question": str(question.get("question") or ""),
        "options": [str(o) for o in question.get("options") or []],
        "explanation": str(question.get("explanation") or ""),
    }


def _hash(source: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(source, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _tokens(text: str) -> List[str]:
    return sorted({m.group(0) for m in _TECHNICAL.finditer(text)})


def _keeps_technical_text(source: str, translated: str) -> bool:
    return all(token in translated for token in _tokens(source))


def _normal(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def accept(source: Dict[str, Any], candidate: Any) -> Optional[Dict[str, Any]]:
    """The candidate as a clean translation, or None when it does not line up with `source`."""
    if not isinstance(candidate, dict):
        return None
    question, options, explanation = candidate.get("question"), candidate.get("options"), candidate.get("explanation", "")
    if not isinstance(question, str) or not question.strip():
        return None
    if not isinstance(options, list) or len(options) != len(source["options"]):
        return None
    if not all(isinstance(o, str) and o.strip() for o in options):
        return None
    if not isinstance(explanation, str) or (source["explanation"].strip() and not explanation.strip()):
        return None
    # Two options that were different must still be different, or the question stops making sense.
    if len({_normal(o) for o in options}) < len({_normal(o) for o in source["options"]}):
        return None
    if not _keeps_technical_text(source["question"], question):
        return None
    if not all(_keeps_technical_text(src, out) for src, out in zip(source["options"], options)):
        return None
    if not _keeps_technical_text(source["explanation"], explanation):
        return None
    return {
        "question": question.strip(),
        "options": [o.strip() for o in options],
        "explanation": explanation.strip(),
    }


def _ask_model(source: Dict[str, Any], language: str) -> Optional[Dict[str, Any]]:
    llm = get_llm()
    for _ in range(2):
        raw = require_text(llm.chat(
            system=SYSTEM.replace("{target}", _NAMES[language]),
            messages=[{"role": "user", "content": json.dumps(source, ensure_ascii=False)}],
            max_tokens=1200,
        ))
        accepted = accept(source, parse_json_response(raw, None))
        if accepted is not None:
            return accepted
    return None


def _store(db: Session, row: Optional[MentorQuizTranslation], quiz_id: int, index: int, language: str, digest: str, payload: Dict[str, Any]) -> None:
    """Keep the translation. Two learners can need the same one at once; the loser of that race
    simply uses its own copy, which is identical in effect."""
    try:
        with db.begin_nested():
            if row is not None:
                row.source_hash, row.payload = digest, payload
            else:
                db.add(MentorQuizTranslation(
                    quiz_id=quiz_id, question_index=index, language=language, source_hash=digest, payload=payload,
                ))
        db.commit()
    except IntegrityError:
        db.rollback()


def translated_question(db: Session, quiz: Quiz, index: int, base: Dict[str, Any], language: str,
                        *, may_call_model: bool = True) -> Optional[Dict[str, Any]]:
    """`base` (the authored question at `index`) in `language`, from the cache or the model.
    None when it could not be produced; the caller then shows the authored text."""
    source = _source(base)
    digest = _hash(source)
    row = (
        db.query(MentorQuizTranslation)
        .filter(
            MentorQuizTranslation.quiz_id == quiz.id,
            MentorQuizTranslation.question_index == index,
            MentorQuizTranslation.language == language,
        )
        .first()
    )
    if row is not None and row.source_hash == digest:
        cached = accept(source, row.payload)
        if cached is not None:
            return cached
        if _recently_failed(row.payload):
            return None
    if not may_call_model:
        # Unverified accounts read cached translations but never cause a
        # provider call: unmetered LLM spend follows the same email gate as
        # metered spend (app/core/authz.py).
        return None
    try:
        fresh = _ask_model(source, language)
    except Exception:
        logger.exception("mentor quiz translation failed; showing the authored text", extra={"quiz_id": quiz.id})
        fresh = None
    if fresh is None:
        logger.warning("mentor quiz translation unavailable", extra={"quiz_id": quiz.id, "question_index": index})
        _store(db, row, quiz.id, index, language, digest, {_FAILED: datetime.now(timezone.utc).isoformat()})
        return None
    _store(db, row, quiz.id, index, language, digest, fresh)
    return fresh


def _recently_failed(payload: Any) -> bool:
    if not isinstance(payload, dict) or _FAILED not in payload:
        return False
    try:
        failed_at = datetime.fromisoformat(str(payload[_FAILED]))
    except ValueError:
        return False
    if failed_at.tzinfo is None:
        failed_at = failed_at.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - failed_at < FAILURE_RETRY_AFTER


def localized(db: Session, quiz: Quiz, index: int, base: Dict[str, Any], chosen: Dict[str, Any], language: Optional[str],
              *, may_call_model: bool = True) -> Tuple[Dict[str, Any], str]:
    """What the learner should read, and the language it is actually in.

    `chosen` is the authored question or its hand-written twin, whichever the quiz offers for
    `language`. When that is already in `language`, it is used as is; otherwise the translation of
    the authored question is, and if there is none, `chosen` with its own language."""
    own = text_language(chosen)
    if language not in LANGUAGES or own == language:
        return chosen, own
    translation = translated_question(db, quiz, index, base, language, may_call_model=may_call_model)
    return (translation, language) if translation else (chosen, own)
