"""
app/views/learning_admin.py

Admin request/response schemas for managing the learning catalogue.

Each `PUT /admin/learning/<kind>/{slug}` body is the *complete* configuration
of that entity, relationship lists included — the same idempotent full-replace
shape the seed script uses — so an admin UI is a form over one object and a
repeat submit is harmless.
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from app.views.learning_path import Slug

_NAME = 200
_TEXT = 4000
_MAX_LINKS = 200


class LevelIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=_NAME)
    name_ar: Optional[str] = Field(None, max_length=_NAME)
    description: Optional[str] = Field(None, max_length=_TEXT)
    description_ar: Optional[str] = Field(None, max_length=_TEXT)
    rank: int = Field(..., ge=1, le=100)
    is_active: bool = True


class FieldIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=_NAME)
    name_ar: Optional[str] = Field(None, max_length=_NAME)
    description: Optional[str] = Field(None, max_length=_TEXT)
    description_ar: Optional[str] = Field(None, max_length=_TEXT)
    icon: Optional[str] = Field(None, max_length=64)
    min_level: Optional[Slug] = None
    prerequisites: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    prerequisite_min_required: int = Field(1, ge=0, le=50)
    prerequisite_recommended: int = Field(1, ge=0, le=50)
    position: int = Field(0, ge=0, le=10_000)
    is_active: bool = True


class CareerGoalIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=_NAME)
    title_ar: Optional[str] = Field(None, max_length=_NAME)
    description: Optional[str] = Field(None, max_length=_TEXT)
    description_ar: Optional[str] = Field(None, max_length=_TEXT)
    icon: Optional[str] = Field(None, max_length=64)
    recommended_level: Optional[Slug] = None
    position: int = Field(0, ge=0, le=10_000)
    is_active: bool = True
    required_fields: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    recommended_fields: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    required_skills: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    optional_skills: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)


class SkillIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=_NAME)
    name_ar: Optional[str] = Field(None, max_length=_NAME)
    # Omitted: a new skill is a 'skill', an existing one keeps its kind.
    kind: Optional[Literal["skill", "tool"]] = None


class CourseSourceIn(BaseModel):
    """Which existing content the course points at: a tool course by slug, or a
    level of a career track by the track's slug and the level's order."""
    kind: Literal["tool_course", "track_level"]
    slug: Optional[Slug] = None
    track_slug: Optional[Slug] = None
    level_order: Optional[int] = Field(None, ge=1, le=1000)


class CourseIn(BaseModel):
    source: CourseSourceIn
    level: Slug
    title: Optional[str] = Field(None, max_length=_NAME)
    title_ar: Optional[str] = Field(None, max_length=_NAME)
    description: Optional[str] = Field(None, max_length=_TEXT)
    description_ar: Optional[str] = Field(None, max_length=_TEXT)
    estimated_hours: Optional[float] = Field(None, ge=0, le=10_000)
    learning_objectives: Optional[List[str]] = Field(None, max_length=50)
    learning_objectives_ar: Optional[List[str]] = Field(None, max_length=50)
    fields: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    roles: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    teaches: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    assumes: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    prerequisites: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    is_active: bool = True


class StageIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=_NAME)
    title_ar: Optional[str] = Field(None, max_length=_NAME)
    description: Optional[str] = Field(None, max_length=_TEXT)
    description_ar: Optional[str] = Field(None, max_length=_TEXT)
    phase: str = Field("specialization", max_length=32)
    kind: Literal["learning", "capstone"] = "learning"
    # Ordered: the position in this list is the order within the stage.
    courses: List[Slug] = Field(default_factory=list, max_length=_MAX_LINKS)
    is_active: bool = True


class TemplateStageIn(BaseModel):
    stage: Slug
    # Only offered when this field is in the learner's route; null = always.
    field: Optional[Slug] = None


class TemplateIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=_NAME)
    title_ar: Optional[str] = Field(None, max_length=_NAME)
    description: Optional[str] = Field(None, max_length=_TEXT)
    description_ar: Optional[str] = Field(None, max_length=_TEXT)
    career_goal: Optional[Slug] = None
    # Ordered: this list IS the path ordering.
    stages: List[TemplateStageIn] = Field(default_factory=list, max_length=_MAX_LINKS)
    is_active: bool = True


# ─── Responses ──────────────────────────────────────────────────────────────

class LevelAdminOut(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    rank: int
    is_active: bool


class SkillAdminOut(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    kind: str = "skill"


class FieldAdminOut(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str] = None
    min_level: Optional[str] = None
    prerequisites: List[str]
    prerequisite_min_required: int
    prerequisite_recommended: int
    position: int
    is_active: bool


class CareerGoalAdminOut(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str] = None
    recommended_level: Optional[str] = None
    position: int
    is_active: bool
    required_fields: List[str]
    recommended_fields: List[str]
    required_skills: List[str]
    optional_skills: List[str]


class StageAdminOut(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    phase: str
    kind: str
    courses: List[str]
    is_active: bool


class TemplateStageOut(BaseModel):
    stage: str
    field: Optional[str] = None


class TemplateAdminOut(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    career_goal: Optional[str] = None
    stages: List[TemplateStageOut]
    is_active: bool


class CourseAdminOut(BaseModel):
    slug: str
    kind: str
    level: str
    title: Optional[str] = None
    fields: List[str]
    roles: List[str]
    teaches: List[str]
    assumes: List[str]
    prerequisites: List[str]
    is_active: bool


class CatalogIssueOut(BaseModel):
    code: str
    subject: object
    detail: Optional[str] = None
