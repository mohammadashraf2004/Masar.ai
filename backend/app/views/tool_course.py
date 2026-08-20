from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.learning import DifficultyLevel
from app.views.learning import LessonResponse, ExerciseResponse, ProjectResponse, QuizResponse


class ToolTopicResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    order: int
    difficulty: DifficultyLevel
    estimated_hours: float
    skill_tags: List[str]
    prerequisite_ids: List[int]
    lessons: List[LessonResponse] = []
    exercises: List[ExerciseResponse] = []
    quizzes: List[QuizResponse] = []
    projects: List[ProjectResponse] = []

    class Config:
        from_attributes = True


class ToolCourseSummary(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    icon: Optional[str]
    category: Optional[str]
    difficulty: DifficultyLevel
    estimated_hours: Optional[float]
    related_track_ids: List[int]
    topic_count: int = 0

    class Config:
        from_attributes = True


class ToolCourseResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    icon: Optional[str]
    category: Optional[str]
    difficulty: DifficultyLevel
    estimated_hours: Optional[float]
    related_track_ids: List[int]
    topics: List[ToolTopicResponse] = []

    class Config:
        from_attributes = True


# ─── Enrollment ────────────────────────────────────────────
class ToolEnrollRequest(BaseModel):
    tool_course_id: int


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
    lesson_id: Optional[int] = None
    exercise_id: Optional[int] = None
    time_spent_minutes: Optional[int] = None


class ToolProgressResponse(BaseModel):
    tool_topic_id: int
    status: str
    lessons_completed: List[int]
    exercises_completed: List[int]
    time_spent_minutes: int

    class Config:
        from_attributes = True
