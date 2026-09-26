"""
app/views/learning_path.py

Request and response schemas for the learning-path API.

Every display string travels as an English field plus its optional `_ar` twin —
the same shape the rest of the API uses (see views/learning.py) — and the
client picks the language it is showing. Nothing here is translated
server-side, and nothing is duplicated per language.

Advisories are returned as a `code` plus parameters, not as sentences. The
wording is interface copy and lives with the other interface strings, in both
languages, on the client.
"""
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated

# Slugs are the public identity of every catalogue entity. Bounded and
# character-restricted here so a path parameter or list entry can never be a
# vehicle for anything but a lookup key.
Slug = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]{0,62}$", max_length=63)]

# A course is addressed by its slug, in any case: `course-004` and `COURSE-004` are the
# same course (the frozen id in the curriculum export is upper-case). Handlers lower-case it.
CourseSlug = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9-]{0,62}$", max_length=63)]

# Nothing in the catalogue comes close to these; they exist to bound a request.
MAX_FIELDS = 12
MAX_SKILLS = 100
MAX_WAIVED = 200

# How much a course matters to one career goal. Mirrors `course_roles.relation`.
TrackRole = Literal["core", "supporting", "optional"]


# ─── Vocabulary ─────────────────────────────────────────────────────────────

class LevelRef(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    rank: int


class LevelOut(LevelRef):
    description: Optional[str] = None
    description_ar: Optional[str] = None


class FieldRef(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    icon: Optional[str] = None


class FieldOut(FieldRef):
    description: Optional[str] = None
    description_ar: Optional[str] = None
    position: int
    # The lowest level offered without a prerequisite route; null = all levels.
    min_level: Optional[LevelRef] = None
    # True when the field starts at the top level — what the UI badges "Advanced".
    is_advanced: bool
    prerequisites: List[FieldRef] = []
    prerequisite_min_required: int
    prerequisite_recommended: int
    course_count: int
    available_course_count: int


class SkillOut(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    # 'skill' is a capability (RAG); 'tool' is a product used to apply one
    # (LangChain). Knowing a tool is not knowing the skill, so the two are told
    # apart wherever skills are listed.
    kind: Literal["skill", "tool"] = "skill"


class SkillOptionOut(SkillOut):
    """A skill offered in "Skills & Technologies I know" for one career goal,
    field route and level."""
    # The field most of the courses teaching it belong to - the section the
    # UI files it under. None for a skill no course in the route teaches.
    group: Optional[FieldRef] = None
    # The career goal lists it as required.
    is_required: bool = False
    # How many courses in this route teach it.
    course_count: int = 0


class RoleRef(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    icon: Optional[str] = None


class CareerGoalOut(RoleRef):
    description: Optional[str] = None
    description_ar: Optional[str] = None
    position: int
    recommended_level: Optional[LevelRef] = None
    required_fields: List[FieldRef] = []
    recommended_fields: List[FieldRef] = []
    required_skills: List[SkillOut] = []
    course_count: int
    available_course_count: int


# ─── Courses ────────────────────────────────────────────────────────────────

class CourseRef(BaseModel):
    id: int
    slug: str
    title: str
    title_ar: Optional[str] = None


class CourseSummary(CourseRef):
    description: Optional[str] = None
    description_ar: Optional[str] = None
    kind: str
    href: Optional[str] = None
    level: LevelRef
    fields: List[FieldRef] = []
    roles: List[RoleRef] = []
    skills: List[SkillOut] = []
    estimated_hours: float
    # The course's structure. Counts only - a listing never carries lesson text.
    module_count: int = 0
    lesson_count: int = 0
    # False for a catalogue entry whose lessons are not published yet.
    is_available: bool
    # Existing catalogue courses are free until an admin activates a paid
    # offer. Paid access itself is reported by the authenticated access API.
    is_free: bool = True
    # The course's weight for one career goal - present only where a goal is in
    # context (a path, or a listing filtered to a single goal), else null. It
    # describes; it never changes a course's state or a path's progress.
    track_role: Optional[TrackRole] = None


class EnrollmentBrief(BaseModel):
    """A signed-in learner's standing in one course. `progress_percentage` is
    derived from their activity on every request, never stored."""
    status: Literal["enrolled", "in_progress", "completed", "paused"]
    progress_percentage: float
    enrolled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ReadinessBrief(BaseModel):
    state: Literal["ready", "mostly_ready", "needs_foundation", "not_assessed"]
    score: int


class CourseCard(CourseSummary):
    """A course in a listing: the summary plus, for a signed-in learner, where
    they stand in it. Still no lesson text."""
    enrollment: Optional[EnrollmentBrief] = None
    readiness: Optional[ReadinessBrief] = None
    # The prerequisites the card names ("Recommended: Machine Learning Foundations").
    recommended_before: List[CourseRef] = []


class ModuleOut(BaseModel):
    id: int                                   # the topic id the course viewer opens
    order: int
    title: str
    title_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    estimated_hours: Optional[float] = None
    lesson_count: int
    exercise_count: int
    quiz_count: int
    project_count: int
    completion_pct: Optional[float] = None    # signed-in learners only
    status: Optional[Literal["not_started", "in_progress", "completed"]] = None


class ProjectOut(BaseModel):
    id: int
    title: str
    title_ar: Optional[str] = None
    estimated_hours: Optional[float] = None
    module_order: int
    kind: Literal["module", "lab", "capstone", "lesson"]


class RoadmapMembership(BaseModel):
    """One roadmap (career goal) this course is part of - informational only."""
    career_goal: RoleRef
    track_role: TrackRole
    position: Optional[int] = None            # 1-based place in that roadmap's order
    total: int = 0                            # courses in that roadmap


class CourseDetail(CourseSummary):
    assumes: List[SkillOut] = []
    # Required prerequisites: the ones a roadmap is ordered by. Never a gate.
    prerequisites: List[CourseRef] = []
    # Advice only.
    recommended_prerequisites: List[CourseRef] = []
    learning_objectives: List[str] = []
    learning_objectives_ar: List[str] = []
    modules: List[ModuleOut] = []
    projects: List[ProjectOut] = []
    roadmaps: List[RoadmapMembership] = []
    enrollment: Optional[EnrollmentBrief] = None


# ─── Paths ──────────────────────────────────────────────────────────────────

class StageRef(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None


# Why a course is on a roadmap (codes, not sentences - the wording is interface
# copy). See services/learning/skill_gaps.py.
CourseReason = Literal[
    "career_requirement", "field_requirement", "stage_requirement", "skill_gap", "prerequisite",
]


class CourseWhyOut(BaseModel):
    """The facts behind "Why this course?" - all read from the catalogue, none
    of them prose. `known_skills` and `skills_to_gain` partition `skills_taught`:
    the first is what the learner *declared*, the second is everything else."""
    career_goal: RoleRef
    # The fields on the learner's route this course belongs to.
    fields: List[FieldRef] = []
    stage: StageRef
    reasons: List[CourseReason] = []
    skills_taught: List[SkillOut] = []
    known_skills: List[SkillOut] = []
    skills_to_gain: List[SkillOut] = []
    # Taught skills the career goal lists as required.
    goal_skills: List[SkillOut] = []
    # Courses still to do on this roadmap that need this one first.
    prerequisite_for: List[CourseRef] = []
    taught_count: int
    known_count: int
    to_gain_count: int


class PathCourseOut(BaseModel):
    # `course.track_role` carries this course's weight for the path's career goal.
    course: CourseSummary
    state: Literal["required", "completed", "optional", "waived"]
    # prerequisite | below_level | known_skills (why it is in this state).
    reason: Optional[str] = None
    completion_pct: Optional[float] = None
    # The skills this course teaches that the learner declared they know. For a
    # waived course this is *why* it is waived; for a required one it shows how
    # much of it they already have.
    known_skills: List[SkillOut] = []
    why: Optional[CourseWhyOut] = None


class RoadmapStep(PathCourseOut):
    """A course located in its stage - what "current" and "next" point at."""
    stage_slug: str
    stage_title: str
    stage_title_ar: Optional[str] = None


class PathStageOut(BaseModel):
    slug: str
    position: int
    title: str
    title_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    phase: str
    kind: str
    # completed | current | upcoming | coming_soon | skippable — derived on the
    # server so the client renders a state instead of re-deriving one.
    status: Literal["completed", "current", "upcoming", "coming_soon", "skippable"]
    progress_pct: Optional[float] = None
    upcoming_count: int = 0
    courses: List[PathCourseOut] = []


class AdvisoryOut(BaseModel):
    code: str
    severity: Literal["info", "warning"]
    params: Dict[str, Any] = {}


class ProgressOut(BaseModel):
    """Progress is a property of the learner's activity, not of a path: a course
    finished once counts everywhere it belongs, and each dimension counts a
    course once."""
    path_pct: Optional[float] = None
    # Counts behind `path_pct`, decided on the server: `path_total` is the
    # required and completed courses (what the percentage is measured over),
    # `path_completed` those already done, `path_known` the ones the learner
    # already knows - shown, but in neither of the other two.
    path_completed: Optional[int] = None
    path_total: Optional[int] = None
    path_known: Optional[int] = None
    overall_pct: float
    by_role: Dict[str, float] = {}
    by_field: Dict[str, float] = {}
    by_skill: Dict[str, float] = {}


class PathOut(BaseModel):
    id: Optional[int] = None
    is_saved: bool
    status: str
    level: LevelRef
    career_goal: RoleRef
    fields: List[FieldRef] = []
    effective_fields: List[FieldRef] = []
    template_slug: Optional[str] = None
    stages: List[PathStageOut] = []
    current_stage_slug: Optional[str] = None
    # The course to work on now (one already in progress, else the first not yet
    # done) and the one after it. Null for a preview, or when nothing is left.
    current_course: Optional[RoadmapStep] = None
    next_course: Optional[RoadmapStep] = None
    # Every required course is done (and there was at least one). Decided here so
    # no client has to infer "finished" from stage statuses.
    is_complete: bool = False
    advisories: List[AdvisoryOut] = []
    estimated_hours: float
    estimated_weeks: int
    progress: Optional[ProgressOut] = None
    generated_at: Optional[datetime] = None


class PathSummaryOut(BaseModel):
    slug: str
    career_goal: RoleRef
    field: Optional[FieldRef] = None
    recommended_level: Optional[LevelRef] = None
    stage_count: int
    course_count: int
    available_course_count: int
    estimated_hours: float


# ─── Learner ────────────────────────────────────────────────────────────────

class ProfileOut(BaseModel):
    level: Optional[LevelRef] = None
    career_goal: Optional[RoleRef] = None
    fields: List[FieldRef] = []
    known_skills: List[SkillOut] = []
    programming_experience: Optional[str] = None
    ai_experience: Optional[str] = None
    onboarding_completed: bool
    # The one flag the client branches on to send someone to onboarding.
    needs_onboarding: bool
    source: str
    has_active_path: bool


SkillStatus = Literal["known", "partially_covered", "missing"]


class SkillGapItemOut(SkillOut):
    """One relevant skill and where the learner stands on it."""
    status: SkillStatus
    # The field most of the roadmap courses teaching it belong to (null: general or a tool).
    group: Optional[FieldRef] = None
    # The earliest roadmap stage that teaches it; null when no course on it does.
    stage: Optional[StageRef] = None
    is_goal_required: bool = False
    # A required course in the current stage teaches it and the learner lacks it.
    is_immediate: bool = False
    # Roadmap courses teaching it. 0 on a goal-required skill: no published course yet.
    course_count: int = 0
    # Not declared, but a course teaching it is finished. Declared and finished stay separate.
    covered_by_completed: bool = False


class SkillGapGroupOut(BaseModel):
    key: str
    # field | general | tools
    kind: Literal["field", "general", "tools"]
    field: Optional[FieldRef] = None
    total: int
    known_count: int
    # What is still to do here: partially covered, then missing.
    skills: List[SkillGapItemOut] = []


class SkillGapSummaryOut(BaseModel):
    required: int = 0
    known: int = 0
    partial: int = 0
    missing: int = 0
    immediate: int = 0
    # Declared share of the relevant skills; null when nothing is relevant.
    coverage_pct: Optional[float] = None


class SkillGapsOut(BaseModel):
    """The learner's gaps against their own roadmap. `available` is false when
    they have no roadmap yet: there is nothing to measure against, and that is an
    ordinary state, not an error."""
    available: bool
    level: Optional[LevelRef] = None
    career_goal: Optional[RoleRef] = None
    fields: List[FieldRef] = []
    current_stage: Optional[StageRef] = None
    summary: SkillGapSummaryOut = SkillGapSummaryOut()
    known: List[SkillGapItemOut] = []
    partial: List[SkillGapItemOut] = []
    missing: List[SkillGapItemOut] = []
    groups: List[SkillGapGroupOut] = []


class LearnerSkillOut(BaseModel):
    skill: SkillOut
    # known | mastered. (`learning` skills are listed separately, derived.)
    status: str
    # self_declared | assessment | course_completion - how we know.
    source: str


class MySkillsOut(BaseModel):
    known: List[LearnerSkillOut] = []
    learning: List[SkillOut] = []


class SkillsUpdate(BaseModel):
    """The learner's whole self-declared list; whatever is absent is removed.

    `skills` itself is required (send `[]` to clear): a body that merely forgot
    the key must not be read as "the learner knows nothing" and wipe the list."""
    skills: List[Slug] = Field(..., max_length=MAX_SKILLS)


class SkillsSavedOut(MySkillsOut):
    # The rebuilt roadmap, or null when the learner has no complete profile yet.
    path: Optional[PathOut] = None
    roadmap_updated: bool = False


class ProfileUpdate(BaseModel):
    """Every key is optional. A key that is *present* replaces that part of the
    profile (null clears level / career goal); a key that is absent leaves it
    alone — the API tells the two apart via `model_fields_set`."""
    level: Optional[Slug] = None
    career_goal: Optional[Slug] = None
    fields: Optional[List[Slug]] = Field(None, max_length=MAX_FIELDS)
    known_skills: Optional[List[Slug]] = Field(None, max_length=MAX_SKILLS)
    # The two questions of the short onboarding. Neither a level nor a career goal is
    # needed to finish it: fields (interests) plus these two answers are enough.
    programming_experience: Optional[Literal["none", "basic", "comfortable", "professional"]] = None
    ai_experience: Optional[Literal["none", "basics", "projects", "applications"]] = None


class GenerateRequest(BaseModel):
    level: Slug
    career_goal: Slug
    fields: List[Slug] = Field(default_factory=list, max_length=MAX_FIELDS)


class PathUpdate(BaseModel):
    """Rebuild the path from the saved profile, or change its status.

    `regenerate` left unset means "whatever the other keys imply": an empty
    body rebuilds, a body carrying only `status` changes just that. Waived
    courses only take effect through a rebuild, so supplying them implies one.
    Asking explicitly for both a rebuild and a status change is refused — a
    rebuilt path is always active, so the two cannot both be honoured."""
    regenerate: Optional[bool] = None
    status: Optional[Literal["active", "paused", "archived"]] = None
    waived_course_ids: Optional[List[int]] = Field(None, max_length=MAX_WAIVED)
