"""
backend/app/content/terminology.py

Server-side access to the AI terminology dictionary.

The dictionary is authored in the frontend (`frontend/src/content/terminology/`)
and exported to `ai_terms.json` next to this module by
`npm run terminology:export`. That direction was chosen because the dictionary
is primarily a *content* asset — it is rendered in lessons, in term cards and
in the glossary — and a single authored copy is the only way "adding a term"
stays a one-file change.

Three server-side consumers:

  * bilingual search  — an Arabic query and its English equivalent must reach
    the same course, without duplicating courses per language.
  * the AI tutor      — its language policy is built from `preferred` terms so
    the tutor uses the same terminology the lessons do.
  * the content lint  — warns an author who wrote "قاعدة بيانات المتجهات"
    where the course should be teaching "Vector Database".

Loaded once at import; the file is a build artefact, not runtime state.
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

_DATA_PATH = Path(__file__).with_name("ai_terms.json")


def _load() -> Dict[str, Any]:
    with _DATA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


_DATA = _load()

TERMS: Dict[str, Dict[str, Any]] = _DATA["terms"]
TECH_NAMES: List[str] = _DATA["tech_names"]
JOB_ROLES: List[Dict[str, Any]] = _DATA["job_roles"]

# ── Normalization ────────────────────────────────────────────────────────
# Mirrors frontend/src/content/terminology/index.ts. The two implementations
# have to agree: a query normalized one way on the client and another way on
# the server would return different results for the same search box.

_AR_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_NON_WORD = re.compile(r"[^\w@+ ]+", re.UNICODE)
_ALEF = re.compile(r"[آأإٱ]")  # آ أ إ ٱ
_YA = re.compile(r"ى")  # ى
_TA_MARBUTA = re.compile(r"ة")  # ة
_HAMZA_SEAT = re.compile(r"[ؤئ]")  # ؤ ئ


def _fold_arabic(value: str) -> str:
    value = _AR_DIACRITICS.sub("", value)
    value = _ALEF.sub("ا", value)
    value = _YA.sub("ي", value)
    value = _TA_MARBUTA.sub("ه", value)
    value = _HAMZA_SEAT.sub("ء", value)
    return value


def _strip_article(word: str) -> str:
    """Drop the Arabic definite article. Handles both the attached form
    ("التضمينات") and the standalone "الـ" that Arabic prose glues onto an
    English term ("الـ Embeddings"), which normalizes to a bare article word
    and is dropped entirely."""
    stripped = re.sub(r"^ال", "", word)
    if not stripped:
        return ""
    return stripped if len(stripped) >= 2 else word


def normalize_term(value: Optional[str]) -> str:
    """Canonical key for any surface form, in either language."""
    if not value:
        return ""
    folded = _fold_arabic(unicodedata.normalize("NFKC", value).lower())
    folded = re.sub(r"[-_/]+", " ", folded)
    folded = _NON_WORD.sub(" ", folded)
    folded = re.sub(r"\s+", " ", folded).strip()
    if not folded:
        return ""
    words = (_strip_article(word) for word in folded.split(" "))
    return " ".join(word for word in words if word).strip()


# ── Index ────────────────────────────────────────────────────────────────


def surface_forms(term: Dict[str, Any]) -> List[str]:
    """Every way a term can be written, in both languages."""
    forms = [term.get("en"), term.get("ar"), term.get("preferred"), term.get("abbreviation")]
    forms.extend(term.get("aliases") or [])
    return [form for form in forms if form]


@lru_cache(maxsize=1)
def _surface_index() -> Dict[str, str]:
    """normalized surface form -> term id. First writer wins, so a term's own
    en/ar/preferred are never shadowed by another term's alias."""
    index: Dict[str, str] = {}
    for term_id, term in TERMS.items():
        for form in surface_forms(term):
            key = normalize_term(form)
            if key and key not in index:
                index[key] = term_id
    return index


def find_term(query: str) -> Optional[Dict[str, Any]]:
    """Resolve any surface form (English, Arabic, abbreviation, alias)."""
    if not query:
        return None
    if query in TERMS:
        return TERMS[query]
    term_id = _surface_index().get(normalize_term(query))
    return TERMS.get(term_id) if term_id else None


def expand_query(query: str) -> Set[str]:
    """Every normalized surface form a search for `query` should also match.

    This is what makes "التضمينات" and "embedding" find the same lesson —
    and what stops the catalogue growing a duplicate Arabic course per
    English one.
    """
    normalized = normalize_term(query)
    if not normalized:
        return set()

    forms = {normalized}
    term = find_term(query)
    if term:
        forms.update(normalize_term(form) for form in surface_forms(term))

    # A multi-word query also matches on its individual known terms, so
    # "بناء RAG pipeline" still hits the RAG material.
    for word in normalized.split(" "):
        word_term = find_term(word)
        if word_term:
            forms.update(normalize_term(form) for form in surface_forms(word_term))

    return {form for form in forms if form}


def expand_query_surfaces(query: str) -> List[str]:
    """Raw (unnormalized) surface forms to match against stored content.

    `expand_query` returns *normalized* keys, which is right for comparing
    two queries but wrong for a SQL `ILIKE '%…%'` against text as authored:
    normalization folds ة→ه and strips the definite article, so the
    normalized key "قاعده بيانات" appears nowhere in the stored string
    "قاعدة بيانات المتجهات". Matching uses the forms as written instead.
    """
    if not query or not query.strip():
        return []

    surfaces = {query.strip()}

    term = find_term(query)
    if term:
        surfaces.update(surface_forms(term))

    for word in query.split():
        word_term = find_term(word)
        if word_term:
            surfaces.update(surface_forms(word_term))

    # Very short fragments match almost everything; the raw query is kept
    # regardless because the user typed it deliberately.
    return [s for s in surfaces if len(s.strip()) >= 2]


def terms_in_query(query: str) -> List[str]:
    """Dictionary ids a search query refers to, in either language."""
    ids = []
    term = find_term(query)
    if term:
        ids.append(term["id"])
    for word in query.split():
        word_term = find_term(word)
        if word_term and word_term["id"] not in ids:
            ids.append(word_term["id"])
    return ids


def terms_in_text(text: str) -> List[str]:
    """Ids of every dictionary term mentioned in a block of text.

    Used to derive a course's technical vocabulary from its own content
    instead of asking every author to maintain a list by hand.
    """
    if not text:
        return []
    normalized = f" {normalize_term(text)} "
    found: List[str] = []
    for term_id, term in TERMS.items():
        for form in surface_forms(term):
            key = normalize_term(form)
            if key and len(key) >= 3 and f" {key} " in normalized:
                found.append(term_id)
                break
    return found


def preferred_of(term_id: str) -> Optional[str]:
    term = TERMS.get(term_id)
    return term.get("preferred") if term else None


def all_terms() -> Iterable[Dict[str, Any]]:
    return TERMS.values()
