"""
app/views/learning_courses.py

Response and request schemas for independent course enrollment, readiness,
recommendations and roadmaps (`app/controllers/learning_courses_controller.py`).

Response shapes are kept apart on purpose - a course summary, a course detail, an
enrollment, a readiness report and a recommendation are different things a
screen asks for - so no endpoint returns one huge nested course object.

Requests carry no score, no readiness and no progress. The only thing a learner
sends is which option they picked (and the enroll/pause intent); everything
else is computed on the server.
"""
from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing_extensions import Annotated

from app.views.learning_path import (
    CareerGoalOut, CourseCard, CourseRef, EnrollmentBrief, ModuleOut, RoleRef, SkillOut, StageRef, TrackRole,
)

ReadinessState = Literal["ready", "mostly_ready", "needs_foundation", "not_assessed"]
SkillLevel = Literal["not_assessed", "beginner", "intermediate", "advanced"]
SkillStanding = Literal["strong", "partial", "gap", "unknown"]
LearningStatus = Literal["enrolled", "in_progress", "completed", "paused"]


# ─── Enrollment ─────────────────────────────────────────────────────────────

class EnrollmentOut(BaseModel):
    course_id: int
    course_slug: str
    status: LearningStatus
    # How access was granted: 'free', 'purchase' or 'admin_grant'.
    source: str
    progress_percentage: float
    enrolled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class EnrollmentUpdate(BaseModel):
    """Pause or resume. The only lifecycle change that is the learner's own."""
    model_config = ConfigDict(extra="forbid")
    status: Literal["paused", "active"]


# ─── Readiness ──────────────────────────────────────────────────────────────

class SkillStandingOut(BaseModel):
    skill: SkillOut
    standing: SkillStanding
    level: SkillLevel
    # Whether a *required* prerequisite teaches it (otherwise a recommended one).
    required: bool


class ReviewModuleOut(BaseModel):
    id: int
    order: int
    title: str
    title_ar: Optional[str] = None


class ReviewOut(BaseModel):
    """A course worth studying first and, inside it, where to start."""
    course: CourseRef
    skills: List[SkillOut] = []
    required: bool
    modules: List[ReviewModuleOut] = []


class ReadinessOut(BaseModel):
    course_id: int
    course_slug: str
    state: ReadinessState
    score: int
    strengths: List[SkillStandingOut] = []
    gaps: List[SkillStandingOut] = []
    recommended_review: List[ReviewOut] = []
    has_prerequisites: bool
    # A short check exists for this course (it has prerequisites with quiz questions).
    assessment_available: bool
    last_assessed_at: Optional[datetime] = None


class ModuleRef(BaseModel):
    id: int
    order: int
    title: str
    title_ar: Optional[str] = None


class StartPlanOut(BaseModel):
    """How to begin, decided from real progress and real readiness.

    `start` = from the first module; `resume` = the learner already has progress,
    so pick up at `recommended_module`. Nothing is marked complete on the
    learner's word, and readiness never removes the option to start now."""
    mode: Literal["start", "resume"]
    recommended_module: Optional[ModuleRef] = None
    preparation: List[ReviewOut] = []


class EnrollOut(BaseModel):
    enrollment: EnrollmentOut
    created: bool
    readiness: ReadinessOut
    start: StartPlanOut


class CourseProgressOut(BaseModel):
    course_id: int
    course_slug: str
    enrolled: bool
    status: LearningStatus
    progress_percentage: float
    modules_total: int
    modules_completed: int
    lessons_total: int
    modules: List[ModuleOut] = []
    next_module: Optional[ModuleRef] = None


# ─── Readiness check ────────────────────────────────────────────────────────

class AssessmentQuestionOut(BaseModel):
    """A question of the check. No answer key, no explanation."""
    id: str
    skill: SkillOut
    question: str
    question_ar: Optional[str] = None
    options: List[str]
    options_ar: Optional[List[str]] = None


class AssessmentOut(BaseModel):
    course_id: int
    course_slug: str
    question_count: int
    estimated_minutes: int
    questions: List[AssessmentQuestionOut]


class AssessmentSubmit(BaseModel):
    """`answers` maps a question id to the index of the option chosen. Nothing
    else is accepted - in particular no score."""
    model_config = ConfigDict(extra="forbid")
    answers: Annotated[Dict[Annotated[str, Field(max_length=24, pattern=r"^\d{1,12}:\d{1,4}$")], StrictInt], Field(max_length=12)]


class QuestionResultOut(BaseModel):
    id: str
    correct: bool
    explanation: str = ""


class AssessmentResultOut(BaseModel):
    assessment_id: int
    score: float
    correct_count: int
    question_count: int
    skill_results: Dict[str, float]
    questions: List[QuestionResultOut]
    readiness: ReadinessOut


# ─── Recommendations ────────────────────────────────────────────────────────

class RecommendationOut(BaseModel):
    course: CourseCard
    # A code the client turns into a sentence in the reader's language ...
    reason_code: str
    params: Dict[str, object] = {}
    # ... and an English sentence for any client that does not.
    reason: str
    readiness: Optional[ReadinessState] = None


class RecommendationsOut(BaseModel):
    continue_learning: List[RecommendationOut] = []
    recommended_next: List[RecommendationOut] = []
    build_foundations: List[RecommendationOut] = []
    completed: List[RecommendationOut] = []
    # The learner's own optional career goal, when they have one.
    career_goal: Optional[RoleRef] = None


# ─── My courses ─────────────────────────────────────────────────────────────

class MyCourseOut(BaseModel):
    course: CourseCard
    enrollment: EnrollmentBrief
    href: Optional[str] = None
    access_type: str


class SkillLevelOut(BaseModel):
    skill: SkillOut
    level: SkillLevel


class SkillLevelsOut(BaseModel):
    """Per-skill proficiency. A learner can be advanced at Python and a beginner
    at machine learning, so this is a list of skills, not one global level."""
    levels: Dict[str, SkillLevel]
    skills: List[SkillLevelOut]
    programming_experience: Optional[str] = None
    ai_experience: Optional[str] = None


# ─── Roadmaps (tracks) ──────────────────────────────────────────────────────

class TrackCourseOut(BaseModel):
    course: CourseCard
    track_role: TrackRole
    position: int
    stage: Optional[StageRef] = None


class TrackDetailOut(CareerGoalOut):
    """A career roadmap: a recommended, ordered collection of courses. It owns
    none of them - each is a canonical course that can be enrolled in directly."""
    courses: List[TrackCourseOut] = []
