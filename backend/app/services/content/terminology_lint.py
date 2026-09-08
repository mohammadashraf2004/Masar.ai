"""
app/services/content/terminology_lint.py

Advisory check on Arabic-first lesson content.

The failure mode this catches is the whole reason the policy exists: an
author writes a perfectly good Arabic sentence — "نستخدم إعادة الترتيب
لتحسين النتائج" — and the student finishes the course able to explain
reranking but unable to recognise the word "Reranking" in a job description,
a paper, or a library's docs.

So the rule is not "don't use Arabic". It is: if you use the Arabic meaning
of a term, the English industry term has to appear too, at least once, so the
student meets both. `Reranking (إعادة الترتيب)` passes. `إعادة الترتيب`
alone warns.

This never blocks publishing. It returns warnings for a human to judge —
some sentences genuinely want the Arabic word and nothing else.
"""
from __future__ import annotations

from typing import Any, Dict, List

from app.content import terminology as T


def _arabic_surfaces(term: Dict[str, Any]) -> List[str]:
    """The Arabic ways of writing a term: its `ar` gloss plus any Arabic
    aliases. English aliases are irrelevant here — they already carry the
    industry terminology."""
    surfaces = [term.get("ar")]
    surfaces.extend(
        alias for alias in (term.get("aliases") or []) if _is_arabic(alias)
    )
    return [s for s in surfaces if s]


def _is_arabic(value: str) -> bool:
    return any("؀" <= char <= "ۿ" for char in value)


def _english_surfaces(term: Dict[str, Any]) -> List[str]:
    """The forms that count as "the industry term was introduced".

    Latin-script aliases count: an author who wrote "vectors" or "fine-tune"
    has put the industry word in front of the student, which is the thing
    being checked, even though it is not the dictionary's preferred spelling.
    """
    surfaces = [term.get("preferred"), term.get("en"), term.get("abbreviation")]
    surfaces.extend(
        alias for alias in (term.get("aliases") or []) if not _is_arabic(alias)
    )
    return [s for s in surfaces if s]


def lint_content(text: str) -> Dict[str, List[Any]]:
    """Return `{"warnings": [...], "terms_used": [...]}` for a block of
    lesson content.

    Code is not excluded from the scan, deliberately: a warning is advisory
    and a term name inside a code fence is still a mention of the term. The
    check only ever *reads* content — it never rewrites it, so it cannot
    damage a code sample.
    """
    warnings: List[Dict[str, str]] = []
    if not text:
        return {"warnings": warnings, "terms_used": []}

    normalized = f" {T.normalize_term(text)} "

    def mentions(surface: str) -> bool:
        key = T.normalize_term(surface)
        return bool(key) and f" {key} " in normalized

    terms_used: List[str] = []

    for term_id, term in T.TERMS.items():
        english_used = any(mentions(surface) for surface in _english_surfaces(term))
        arabic_used = next(
            (surface for surface in _arabic_surfaces(term) if mentions(surface)),
            None,
        )

        if english_used or arabic_used:
            terms_used.append(term_id)

        if arabic_used and not english_used:
            preferred = term["preferred"]
            warnings.append(
                {
                    "term_id": term_id,
                    "found": arabic_used,
                    "suggestion": f'{preferred} ({term["ar"]})',
                    "message": (
                        f'استخدمت «{arabic_used}» دون ذكر المصطلح الإنجليزي. '
                        f'قدّمه مرة واحدة على الأقل بصيغة «{preferred} ({term["ar"]})» '
                        f'ثم استمر في استخدام «{preferred}».'
                    ),
                }
            )

    return {"warnings": warnings, "terms_used": sorted(terms_used)}
