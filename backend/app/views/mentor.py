from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Every field below that reaches an LLM is length-capped. These strings
# are pasted verbatim into a provider prompt, so their size is a direct,
# caller-chosen multiplier on our per-request token bill — and an
# uncapped one is an "unlimited spend" button for any account holder.
# The caps mirror INPUT_DEFAULT_MAX_CHARACTERS, which the providers now
# also enforce as a backstop (see BaseLLMProvider.clip_input).
MAX_MESSAGE_CHARS = 10_000
MAX_CODE_CHARS = 20_000
MAX_CV_CHARS = 20_000


class MentorMessage(BaseModel):
    content: str = Field(..., min_length=1, max_length=MAX_MESSAGE_CHARS)
    topic_id: Optional[int] = Field(None, gt=0)  # context hint
    # The student's language settings, forwarded so the mentor answers the
    # way their lessons are written. Both optional and pattern-bounded; the
    # service falls back to the Arabic-first default for anything else, and
    # they only ever select prompt text — never free-form prompt content.
    language: Optional[str] = Field(None, pattern="^(ar|en)$")
    terminology_mode: Optional[str] = Field(
        None, pattern="^(arabic_first|industry|english_technical)$"
    )


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
    code: str = Field(..., min_length=1, max_length=MAX_CODE_CHARS)
    language: str = Field("python", max_length=40)
    context: Optional[str] = Field(None, max_length=2_000)  # what the code is supposed to do


class CodeReviewResponse(BaseModel):
    overall_quality: str
    score: int  # 0-100
    issues: List[dict]  # [{type, severity, line, message, suggestion}]
    strengths: List[str]
    improvements: List[str]
    summary: str


class SkillGapRequest(BaseModel):
    cv_text: Optional[str] = Field(None, max_length=MAX_CV_CHARS)
    github_url: Optional[str] = Field(None, max_length=500)
    target_role: str = Field("AI Engineer", max_length=120)
    current_skills: List[str] = Field(default_factory=list, max_length=100)


class SkillGapResponse(BaseModel):
    target_role: str
    current_skills: List[str]
    missing_skills: List[dict]  # [{skill, priority, reason}]
    recommended_roadmap: List[str]
    readiness_score: int  # 0-100
    summary: str


class MockInterviewRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)  # "ML concepts", "system design", ...
    difficulty: str = Field("intermediate", max_length=40)
    previous_qa: List[dict] = Field(default_factory=list, max_length=50)  # ongoing interview


class MockInterviewResponse(BaseModel):
    question: str
    question_type: str
    hints: List[str]
    follow_up: Optional[str] = None
