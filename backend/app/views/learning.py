from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime
from app.models.learning import DifficultyLevel

# Keys inside a quiz question's JSON that constitute the answer key.
# Stripped from every response that carries questions, because the same
# `questions` blob is used both to render the quiz and to grade it.
_ANSWER_KEY_FIELDS = ("correct", "correct_answer", "answer", "explanation", "solution")


def list_or_empty(value):
    """JSON list columns added by migration 006 are NULL on rows that predate
    it. Every response model treats that as an empty list rather than making
    the field Optional at every call site."""
    return value or []


def _strip_answer_key(questions):
    if not questions:
        return []
    return [
        {k: v for k, v in q.items() if k not in _ANSWER_KEY_FIELDS}
        if isinstance(q, dict) else q
        for q in questions
    ]


class LessonResponse(BaseModel):
    """The Arabic twins are optional on every content model: a lesson that
    has no Arabic version returns null and the client falls back to the
    English original (and says so). Code fields have no twin — see
    docs/content/ARABIC_FIRST_GUIDELINES.md."""
    id: int
    title: str
    content: str
    title_ar: Optional[str] = None
    content_ar: Optional[str] = None
    order: int
    estimated_minutes: int
    has_code_examples: bool

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: int
    title: str
    description: str
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    starter_code: Optional[str]
    difficulty: DifficultyLevel
    skill_tested: List[str]

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    difficulty: DifficultyLevel
    tech_stack: List[str]
    objectives: List[str]
    rubric: dict
    starter_repo_url: Optional[str]
    estimated_hours: float

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    """A quiz as the *taker* is allowed to see it.

    Quiz.questions is a single JSON blob holding both the prompt and the
    answer key ("correct", "explanation"). It was previously returned
    verbatim by GET /tracks/{slug} and GET /tracks/topics/{id}, so anyone
    could read every answer before submitting — and the same blob feeds
    the certification-track quizzes. The stripping happens here, on the
    response model, so every endpoint that returns a quiz gets it, rather
    than depending on each controller to remember.
    """
    id: int
    title: str
    questions: List[dict]
    title_ar: Optional[str] = None
    # The Arabic questions blob carries the same answer key as `questions`,
    # so it goes through exactly the same stripping. Adding a second copy of
    # the questions without this would have re-opened the leak the English
    # validator was written to close.
    questions_ar: Optional[List[dict]] = None
    passing_score: int

    @field_validator("questions", mode="before")
    @classmethod
    def _strip_en(cls, questions):
        return _strip_answer_key(questions)

    @field_validator("questions_ar", mode="before")
    @classmethod
    def _strip_ar(cls, questions):
        return _strip_answer_key(questions) if questions else None

    class Config:
        from_attributes = True


class TopicResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    order: int
    difficulty: DifficultyLevel
    estimated_hours: float
    prerequisite_ids: List[int]
    skill_tags: List[str]
    # Terminology dictionary ids this topic teaches.
    technical_terms: List[str] = []
    lessons: List[LessonResponse] = []
    exercises: List[ExerciseResponse] = []
    projects: List[ProjectResponse] = []
    quizzes: List[QuizResponse] = []

    @field_validator("technical_terms", mode="before")
    @classmethod
    def _terms_or_empty(cls, value):
        return list_or_empty(value)

    class Config:
        from_attributes = True


class TrackLevelResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    order: int
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True


class CareerTrackResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str]
    estimated_weeks: int
    levels: List[TrackLevelResponse] = []

    class Config:
        from_attributes = True


class CareerTrackSummary(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str]
    estimated_weeks: int

    class Config:
        from_attributes = True


# ─── Enrollment ────────────────────────────────────────────
class EnrollRequest(BaseModel):
    track_id: int = Field(..., gt=0)
    target_job_title: Optional[str] = Field(None, max_length=200)


class EnrollmentResponse(BaseModel):
    id: int
    track_id: int
    track: CareerTrackSummary
    completion_percentage: float
    enrolled_at: datetime
    target_job_title: Optional[str]

    class Config:
        from_attributes = True


# ─── Progress ──────────────────────────────────────────────
class ProgressUpdate(BaseModel):
    lesson_id: Optional[int] = Field(None, gt=0)
    exercise_id: Optional[int] = Field(None, gt=0)
    # Self-reported study time feeds the scorecard's total_study_minutes.
    # One call can't add more than a day's worth; the controller also
    # caps the running total. Unbounded, a client could report a
    # multi-million-minute session (or a negative one, subtracting time).
    time_spent_minutes: Optional[int] = Field(None, ge=0, le=1440)


class ProgressResponse(BaseModel):
    topic_id: int
    status: str
    lessons_completed: List[int]
    exercises_completed: List[int]
    time_spent_minutes: int

    class Config:
        from_attributes = True


# ─── Quiz Attempt ──────────────────────────────────────────
class QuizSubmit(BaseModel):
    # {question_index: selected_option_index}. Bounded: the answers dict
    # is persisted verbatim on the attempt row, so an unbounded map is a
    # free write-amplification primitive against the database.
    answers: dict = Field(..., max_length=200)


class QuizAttemptResponse(BaseModel):
    id: int
    score: float
    passed: bool
    feedback: dict
    attempted_at: datetime

    class Config:
        from_attributes = True


# ─── Project Submission ────────────────────────────────────
class ProjectSubmit(BaseModel):
    """A project is submitted as code, written in the reader's code cell.

    `github_url` is deliberately absent: a repo link was never what the
    reviewer read (the old `description` field was), so asking for one
    promised a review of a repository that nothing ever fetched.
    """
    # Required, and non-blank: a submission without code is not a project
    # submission, and silently accepting one is what used to make the
    # button look broken (saved, but nothing to review).
    #
    # This string is forwarded straight to the LLM code reviewer, so its
    # length is a direct, attacker-chosen multiplier on our per-request
    # token spend. Capped at roughly the largest file a student would
    # plausibly write in a cell.
    code: str = Field(..., min_length=1, max_length=20_000)
    # Optional notes on approach — context for the reviewer, not the
    # thing being reviewed, so it gets a much smaller budget.
    description: Optional[str] = Field(None, max_length=2_000)

    @field_validator("code", mode="after")
    @classmethod
    def _non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Write some code before submitting.")
        return v


class ProjectHintRequest(BaseModel):
    """Same shape as the challenge hint request — a student asking for
    help on a project is asking the same kind of question."""
    stuck_on: str = Field(..., min_length=1, max_length=1_000)
    # Whatever is currently in their code cell. Optional: a student can
    # ask for a hint before writing a line. Capped like `code` above.
    code: Optional[str] = Field(None, max_length=20_000)
    # Hints already given, so the tutor doesn't repeat itself. Bounded on
    # both axes — this is echoed straight back into the prompt.
    previous_hints: List[str] = Field(default_factory=list, max_length=20)
    language: Optional[str] = None
    terminology_mode: Optional[str] = None


class ProjectHintResponse(BaseModel):
    hint: str
    concept: str = ""
    next_step: str = ""


class ProjectSubmissionResponse(BaseModel):
    id: int
    project_id: int
    code: Optional[str]
    description: Optional[str]
    ai_review: Optional[dict]
    score: Optional[float]
    submitted_at: datetime

    class Config:
        from_attributes = True


# ─── Skill Scores ──────────────────────────────────────────
class SkillScoreResponse(BaseModel):
    skill_name: str
    score: float
    last_assessed_at: datetime

    class Config:
        from_attributes = True
