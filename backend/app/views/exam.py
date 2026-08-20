from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from app.models.exam import ExamStatus, ViolationType


# ─── Exam info (shown before starting) ───────────────────────────────────────
class ExamInfoResponse(BaseModel):
    id: int
    track_id: int
    title: str
    description: Optional[str]
    duration_minutes: int
    passing_score: int
    max_attempts: int
    total_questions: int
    attempts_used: int         # injected per user
    can_attempt: bool          # injected per user

    class Config:
        from_attributes = True


# ─── Exam session (questions, no answers) ────────────────────────────────────
class ExamQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    points: int
    type: str                  # mcq | code | scenario


class ExamSessionResponse(BaseModel):
    attempt_id: int
    exam_id: int
    title: str
    duration_minutes: int
    questions: List[ExamQuestion]
    started_at: datetime


# ─── Submit answers ───────────────────────────────────────────────────────────
class ExamSubmit(BaseModel):
    answers: Dict[str, int]    # {question_id: selected_option_index}
    time_spent_seconds: int


# ─── Proctoring violation ─────────────────────────────────────────────────────
class ViolationReport(BaseModel):
    violation: ViolationType
    description: Optional[str] = None


# ─── Result ───────────────────────────────────────────────────────────────────
class QuestionResult(BaseModel):
    question_id: int
    question: str
    your_answer: Optional[int]
    correct_answer: int
    is_correct: bool
    explanation: str
    points: int


class ExamResultResponse(BaseModel):
    attempt_id: int
    status: ExamStatus
    score: float
    passed: bool
    passing_score: int
    violations_count: int
    tab_switches: int
    face_warnings: int
    time_spent_seconds: Optional[int]
    question_results: List[QuestionResult]
    certificate_id: Optional[str] = None   # set if passed


# ─── Certificate ──────────────────────────────────────────────────────────────
class CertificateResponse(BaseModel):
    certificate_id: str
    track_title: str
    user_name: str
    score: float
    issued_at: datetime
    is_valid: bool

    class Config:
        from_attributes = True


# ─── Attempt summary ──────────────────────────────────────────────────────────
class AttemptSummary(BaseModel):
    id: int
    status: ExamStatus
    score: Optional[float]
    passed: Optional[bool]
    violations_count: int
    started_at: Optional[datetime]
    submitted_at: Optional[datetime]

    class Config:
        from_attributes = True