from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from app.models.learning import DifficultyLevel


class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    order: int
    estimated_minutes: int
    has_code_examples: bool

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: int
    title: str
    description: str
    starter_code: Optional[str]
    difficulty: DifficultyLevel
    skill_tested: List[str]

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: DifficultyLevel
    tech_stack: List[str]
    objectives: List[str]
    rubric: dict
    starter_repo_url: Optional[str]
    estimated_hours: float

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: int
    title: str
    questions: List[dict]
    passing_score: int

    class Config:
        from_attributes = True


class TopicResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    order: int
    difficulty: DifficultyLevel
    estimated_hours: float
    prerequisite_ids: List[int]
    skill_tags: List[str]
    lessons: List[LessonResponse] = []
    exercises: List[ExerciseResponse] = []
    projects: List[ProjectResponse] = []

    class Config:
        from_attributes = True


class TrackLevelResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    order: int
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True


class CareerTrackResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
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
    icon: Optional[str]
    estimated_weeks: int

    class Config:
        from_attributes = True


# ─── Enrollment ────────────────────────────────────────────
class EnrollRequest(BaseModel):
    track_id: int
    target_job_title: Optional[str] = None


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
    lesson_id: Optional[int] = None
    exercise_id: Optional[int] = None
    time_spent_minutes: Optional[int] = None


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
    answers: dict  # {question_index: selected_option_index}


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
    github_url: Optional[str] = None
    description: Optional[str] = None


class ProjectSubmissionResponse(BaseModel):
    id: int
    project_id: int
    github_url: Optional[str]
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
