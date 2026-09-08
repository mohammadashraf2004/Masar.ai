from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.learning import DifficultyLevel
from app.views.learning import (
    LessonResponse, ExerciseResponse, ProjectResponse, QuizResponse,
    list_or_empty,
)


class ToolTopicResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    order: int
    difficulty: DifficultyLevel
    estimated_hours: float
    skill_tags: List[str]
    technical_terms: List[str] = []
    prerequisite_ids: List[int]
    lessons: List[LessonResponse] = []
    exercises: List[ExerciseResponse] = []
    quizzes: List[QuizResponse] = []
    projects: List[ProjectResponse] = []

    @field_validator("technical_terms", mode="before")
    @classmethod
    def _terms_or_empty(cls, value):
        return list_or_empty(value)

    class Config:
        from_attributes = True


class ToolCourseSummary(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str]
    category: Optional[str]
    difficulty: DifficultyLevel
    estimated_hours: Optional[float]
    related_track_ids: List[int]
    # Terminology dictionary ids the course teaches, and the skill labels a
    # recruiter would search for. Both empty on courses seeded before
    # migration 006 — the browse page just shows no vocabulary panel.
    technical_terms: List[str] = []
    industry_skills: List[str] = []
    topic_count: int = 0

    @field_validator("technical_terms", "industry_skills", mode="before")
    @classmethod
    def _lists_or_empty(cls, value):
        return list_or_empty(value)

    class Config:
        from_attributes = True


class ToolCourseResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str]
    category: Optional[str]
    difficulty: DifficultyLevel
    estimated_hours: Optional[float]
    related_track_ids: List[int]
    technical_terms: List[str] = []
    industry_skills: List[str] = []
    topics: List[ToolTopicResponse] = []

    @field_validator("technical_terms", "industry_skills", mode="before")
    @classmethod
    def _lists_or_empty(cls, value):
        return list_or_empty(value)

    class Config:
        from_attributes = True


# ─── Enrollment ────────────────────────────────────────────
class ToolEnrollRequest(BaseModel):
    tool_course_id: int = Field(..., gt=0)


class ToolEnrollmentResponse(BaseModel):
    id: int
    tool_course_id: int
    tool_course: ToolCourseSummary
    progress_pct: float
    enrolled_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─── Progress ──────────────────────────────────────────────
class ToolProgressUpdate(BaseModel):
    lesson_id: Optional[int] = Field(None, gt=0)
    exercise_id: Optional[int] = Field(None, gt=0)
    # See app.views.learning.ProgressUpdate — self-reported, so bounded.
    time_spent_minutes: Optional[int] = Field(None, ge=0, le=1440)


class ToolProgressResponse(BaseModel):
    tool_topic_id: int
    status: str
    lessons_completed: List[int]
    exercises_completed: List[int]
    time_spent_minutes: int

    class Config:
        from_attributes = True
