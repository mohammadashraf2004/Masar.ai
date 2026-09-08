from typing import Dict, List, Optional

from pydantic import BaseModel, Field

# A student can meet a lot of terms in one lesson, but not hundreds — the
# cap bounds a single request's write amplification against user_term_progress
# the same way the quiz answers map is bounded in views/learning.py.
MAX_TERMS_PER_REQUEST = 100
MAX_LINT_CHARS = 60_000


class TermEntry(BaseModel):
    """One dictionary entry, served as authored.

    The dictionary itself lives in app/content/ai_terms.json (generated from
    the frontend source), so this model exists to give the endpoint a schema,
    not to reshape the data.
    """
    id: str
    en: str
    ar: str
    preferred: str
    abbreviation: Optional[str] = None
    category: str
    level: str
    aliases: List[str] = []
    definitionAr: str
    definitionEn: str
    exampleAr: Optional[str] = None


class TerminologyResponse(BaseModel):
    version: int
    terms: List[TermEntry]
    tech_names: List[str]


class VocabularyProgressResponse(BaseModel):
    """Both lists are term ids. `encountered` includes everything in
    `learned` — a term cannot be proven without having been met."""
    encountered: List[str]
    learned: List[str]
    total_terms: int


class VocabularyRecordRequest(BaseModel):
    term_ids: List[str] = Field(..., min_length=1, max_length=MAX_TERMS_PER_REQUEST)
    status: str = Field("encountered", pattern="^(encountered|learned)$")


class TerminologyWarning(BaseModel):
    """One content-lint finding. Advisory: it never blocks publishing."""
    term_id: str
    found: str
    suggestion: str
    message: str


class TerminologyLintRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_LINT_CHARS)


class TerminologyLintResponse(BaseModel):
    warnings: List[TerminologyWarning]
    #: Dictionary ids detected in the text — an author can paste this
    #: straight into a course's `technical_terms`.
    terms_used: List[str]


# ─── Bilingual search ────────────────────────────────────────────────────

class SearchHit(BaseModel):
    kind: str  # "tool_course" | "tool_topic" | "track" | "topic" | "lesson"
    id: int
    title: str
    title_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    #: Where to navigate, e.g. "/tools/langchain".
    href: str
    #: Course/track this hit belongs to, for display.
    parent_title: Optional[str] = None
    score: float
    matched_terms: List[str] = []


class SearchResponse(BaseModel):
    query: str
    #: The normalized surface forms the query was expanded into. Returned so
    #: the UI can show "searched also for: Embeddings, التضمينات".
    expanded: List[str]
    matched_terms: List[TermEntry] = []
    hits: List[SearchHit]
