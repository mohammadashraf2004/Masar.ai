"""
app/services/learning/domain.py

Plain, immutable value objects the learning services pass around.

The catalogue is read from the database once per request into a `Catalog`
snapshot, and the path generator works on that snapshot alone. Two payoffs:
the rules can be unit-tested with a hand-built `Catalog` and no session, and a
generation can never issue a query that depends on iteration order or on a
lazy load firing halfway through a decision.

Nothing here knows about HTTP, SQLAlchemy or translations. Display names are
resolved at the API boundary from the ORM rows; the domain only reasons about
slugs and ids.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

# ── Course states inside a path ──────────────────────────────────────────────
STATE_REQUIRED = "required"      # on the route, not yet done
STATE_COMPLETED = "completed"    # the learner has finished it
STATE_OPTIONAL = "optional"      # below their level and not needed to close a gap
STATE_WAIVED = "waived"          # the learner said they already know it

# States that count toward progress. Optional and waived courses are visible
# but never in the denominator — skipping one must not lower a percentage.
COUNTED_STATES = frozenset({STATE_REQUIRED, STATE_COMPLETED})

# Why a course is waived, when it is not an explicit per-course waiver.
# 'known_skills': the learner declared every skill the course teaches.
REASON_KNOWN_SKILLS = "known_skills"

# ── Advisory codes ───────────────────────────────────────────────────────────
# The API returns codes plus parameters; wording is UI copy and lives with the
# rest of the interface strings, in both languages.
ADVISORY_FIELD_ABOVE_LEVEL = "field_above_level"
ADVISORY_PREREQUISITE_ROUTE_ADDED = "prerequisite_route_added"
ADVISORY_PREREQUISITES_RECOMMENDED = "prerequisites_recommended"
ADVISORY_PREREQUISITE_ORDER = "prerequisite_out_of_order"
ADVISORY_PREREQUISITE_CYCLE = "prerequisite_cycle"
ADVISORY_NO_TEMPLATE = "no_template_fallback"
ADVISORY_NO_AVAILABLE_COURSES = "no_available_courses"


@dataclass(frozen=True)
class LevelInfo:
    id: int
    slug: str
    rank: int


@dataclass(frozen=True)
class FieldInfo:
    id: int
    slug: str
    position: int
    min_level_rank: Optional[int]
    prerequisite_slugs: Tuple[str, ...] = ()
    prerequisite_min_required: int = 1
    prerequisite_recommended: int = 1


@dataclass(frozen=True)
class RoleInfo:
    id: int
    slug: str
    recommended_level_rank: Optional[int]
    required_field_slugs: Tuple[str, ...] = ()
    recommended_field_slugs: Tuple[str, ...] = ()
    required_skill_slugs: FrozenSet[str] = frozenset()


@dataclass(frozen=True)
class CourseRoleWorkflow:
    role_slug: str
    relation: str
    position: int
    required: bool
    section: Optional[str] = None


@dataclass(frozen=True)
class CourseInfo:
    id: int
    slug: str
    level_rank: int
    field_slugs: FrozenSet[str] = frozenset()
    role_slugs: FrozenSet[str] = frozenset()
    # (career goal slug, 'core' | 'supporting' | 'optional'), sorted. Descriptive
    # metadata for display and discovery: no generation rule reads it.
    role_relations: Tuple[Tuple[str, str], ...] = ()
    # (career goal slug, relation, position, required, section) - the same
    # relationship with its workflow placement. `position` is this goal's own
    # explicit order (never this course's id, never alphabetical); `section`
    # is only set for goals whose workflow reads in named parts.
    role_workflow: Tuple["CourseRoleWorkflow", ...] = ()
    teaches: FrozenSet[str] = frozenset()
    assumes: FrozenSet[str] = frozenset()
    # Required prerequisites: the only ones the path generator orders a roadmap by.
    prerequisite_ids: FrozenSet[int] = frozenset()
    # Advice only (readiness, recommendations); never read by the path generator.
    recommended_prerequisite_ids: FrozenSet[int] = frozenset()
    estimated_hours: float = 0.0
    # Structure of the course's content: modules (topics) and lessons. Counts only -
    # a catalogue snapshot never carries lesson bodies.
    module_count: int = 0
    lesson_count: int = 0
    # Active AND its source actually contains lessons. A catalogue entry whose
    # content has not been written yet is *planned*, not available: it is
    # never put in front of a learner as something they can start.
    is_available: bool = True
    is_active: bool = True

    def relation_for(self, role_slug: str) -> Optional[str]:
        """This course's weight in one career goal, or None when it is not tagged for it."""
        return next((rel for slug, rel in self.role_relations if slug == role_slug), None)

    def workflow_for(self, role_slug: str) -> Optional["CourseRoleWorkflow"]:
        """This course's full workflow placement in one career goal's track,
        or None when it is not part of that goal's workflow."""
        return next((w for w in self.role_workflow if w.role_slug == role_slug), None)


@dataclass(frozen=True)
class StageInfo:
    slug: str
    phase: str
    kind: str
    course_ids: Tuple[int, ...] = ()


@dataclass(frozen=True)
class TemplateStageInfo:
    stage: StageInfo
    field_slug: Optional[str] = None


@dataclass(frozen=True)
class TemplateInfo:
    slug: str
    role_slug: Optional[str]
    stages: Tuple[TemplateStageInfo, ...] = ()


@dataclass(frozen=True)
class Catalog:
    levels: Dict[str, LevelInfo] = field(default_factory=dict)
    fields: Dict[str, FieldInfo] = field(default_factory=dict)
    roles: Dict[str, RoleInfo] = field(default_factory=dict)
    courses: Dict[int, CourseInfo] = field(default_factory=dict)
    # Keyed by career-goal slug; `None` holds the fallback template.
    templates: Dict[Optional[str], TemplateInfo] = field(default_factory=dict)
    # Slugs of skills whose `kind` is 'tool' (a product, not a capability).
    # Tools are ordinary skills to every rule; this only lets a reader of the
    # snapshot tell them apart (skill-gap grouping) without a second lookup.
    tools: FrozenSet[str] = frozenset()

    def available_courses_in_field(self, slug: str) -> List[CourseInfo]:
        return [c for c in self.courses.values() if c.is_available and slug in c.field_slugs]


@dataclass(frozen=True)
class UserState:
    """What the learner has done and said, as far as path generation cares.

    `known_skill_slugs` is what the learner *declared*. It is kept apart from
    what their finished courses taught them (which the generator derives from
    `completed_course_ids`) because only a declaration may waive a course:
    completing two courses must not silently waive a third that happens to
    teach the union of their skills."""

    completed_course_ids: FrozenSet[int] = frozenset()
    known_skill_slugs: FrozenSet[str] = frozenset()
    waived_course_ids: FrozenSet[int] = frozenset()


EMPTY_STATE = UserState()


# ── Output ───────────────────────────────────────────────────────────────────

@dataclass
class PlannedCourse:
    course_id: int
    state: str
    # Why it is in this state, when that is not obvious: 'prerequisite'
    # (pulled in to satisfy another course), 'below_level' (optional).
    reason: Optional[str] = None


@dataclass
class PlannedStage:
    slug: str
    position: int
    phase: str
    kind: str
    courses: List[PlannedCourse] = field(default_factory=list)
    # Courses configured for this stage whose content is not published yet.
    upcoming_count: int = 0


@dataclass
class Advisory:
    code: str
    severity: str = "info"          # info | warning
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PathPlan:
    level_slug: str
    role_slug: str
    field_slugs: List[str]              # what the learner asked for
    effective_field_slugs: List[str]    # requested + any prerequisite routes added
    template_slug: Optional[str]
    stages: List[PlannedStage] = field(default_factory=list)
    advisories: List[Advisory] = field(default_factory=list)
    estimated_hours: float = 0.0        # remaining effort: required, not yet completed
