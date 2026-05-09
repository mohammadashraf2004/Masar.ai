from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MentorMessage(BaseModel):
    content: str
    topic_id: Optional[int] = None  # context hint


class MentorResponse(BaseModel):
    session_id: int
    reply: str
    suggested_actions: List[str] = []


class MentorSessionResponse(BaseModel):
    id: int
    title: Optional[str]
    messages: List[dict]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    context: Optional[str] = None  # what the code is supposed to do


class CodeReviewResponse(BaseModel):
    overall_quality: str
    score: int  # 0-100
    issues: List[dict]  # [{type, severity, line, message, suggestion}]
    strengths: List[str]
    improvements: List[str]
    summary: str


class SkillGapRequest(BaseModel):
    cv_text: Optional[str] = None
    github_url: Optional[str] = None
    target_role: str = "AI Engineer"
    current_skills: List[str] = []


class SkillGapResponse(BaseModel):
    target_role: str
    current_skills: List[str]
    missing_skills: List[dict]  # [{skill, priority, reason}]
    recommended_roadmap: List[str]
    readiness_score: int  # 0-100
    summary: str


class MockInterviewRequest(BaseModel):
    topic: str  # "ML concepts", "system design", "coding", "behavioral"
    difficulty: str = "intermediate"
    previous_qa: List[dict] = []  # ongoing interview


class MockInterviewResponse(BaseModel):
    question: str
    question_type: str
    hints: List[str]
    follow_up: Optional[str] = None
