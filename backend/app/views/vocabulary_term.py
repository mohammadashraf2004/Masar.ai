"""
backend/app/views/vocabulary_term.py

Schemas for the normalized AI Vocabulary dictionary (migration 022) — separate
from `views/terminology.py`, which stays as the schema for the legacy
`ai_terms.json` endpoints (`/terminology/*`) that the vocabulary progress
system still uses under the hood.
"""
from typing import List, Optional

from pydantic import BaseModel

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 24


class CourseMapping(BaseModel):
    course_key: str
    course_title: Optional[str] = None
    course_href: Optional[str] = None
    #: True when at least one association for this (term, course) pair points
    #: at a real lesson — COURSE-006 is outline-only, so its associations are
    #: course/module-level only and this is always False for it. The
    #: frontend must not offer a "Learn this concept" action when this is
    #: False, even though `course_href` (a link to the course itself) may
    #: still be set.
    has_lesson_mapping: bool = False


class LessonMapping(BaseModel):
    course_key: str
    module_key: Optional[str] = None
    lesson_key: str
    lesson_title: Optional[str] = None
    #: Where to open it, when the lesson is a real, currently-imported row —
    #: never fabricated. None means the mapping is known but the lesson isn't
    #: (yet) resolvable to a live route.
    href: Optional[str] = None


class RelatedTerm(BaseModel):
    slug: str
    term_en: str
    term_ar: str


class TermProgressState(BaseModel):
    status: str  # "new" | "learning" | "mastered"


class VocabularyTermSummary(BaseModel):
    """The list DTO — lightweight, no explanations or mappings."""
    slug: str
    term_en: str
    term_ar: str
    acronym: Optional[str] = None
    explanation_simple_ar: Optional[str] = None
    definition_en: str
    definition_ar: str
    category: Optional[str] = None
    difficulty: str
    course_count: int
    progress: Optional[TermProgressState] = None


class VocabularyTermDetail(BaseModel):
    """The detail DTO — everything."""
    slug: str
    term_en: str
    term_ar: str
    acronym: Optional[str] = None
    aliases: List[str] = []
    category: Optional[str] = None
    difficulty: str
    tags: List[str] = []
    definition_en: str
    definition_ar: str
    explanation_simple_ar: Optional[str] = None
    why_it_matters_ar: Optional[str] = None
    example_ar: Optional[str] = None
    related_terms: List[RelatedTerm] = []
    courses: List[CourseMapping] = []
    first_introduced: Optional[LessonMapping] = None
    progress: Optional[TermProgressState] = None


class VocabularyListResponse(BaseModel):
    items: List[VocabularyTermSummary]
    total: int
    page: int
    page_size: int


class CategoryCount(BaseModel):
    category: str
    term_count: int


class VocabularyCategoriesResponse(BaseModel):
    categories: List[str]
    #: Same categories, each with its active-term count — additive field so
    #: existing callers that only read `categories` are unaffected. Powers
    #: "Browse by Category" without a second endpoint.
    counts: List[CategoryCount] = []


class CourseCount(BaseModel):
    course_key: str
    term_count: int
    course_title: Optional[str] = None
    #: The ToolCourse slug (e.g. "applied-llm-engineering") — lets the
    #: frontend match a learner's already-known enrolled/active course slug
    #: back to this course's vocabulary without a second recommendation
    #: engine or a hardcoded course-id table.
    course_slug: Optional[str] = None
    course_href: Optional[str] = None


class VocabularyCourseCountsResponse(BaseModel):
    courses: List[CourseCount]


class VocabularyTermProgressRequest(BaseModel):
    status: str
