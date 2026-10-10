from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AnswerMessage(BaseModel):
    # Forwarded to the LLM grader — capped for the same reason as
    # app.views.mentor.MentorMessage.content.
    content: str = Field(..., min_length=1, max_length=10_000)
    # The student's language settings. The grader is a tutor too, so it
    # follows the same policy the lessons and the mentor do: Arabic
    # explanation, English terminology, untouched code. Pattern-bounded;
    # anything else falls back to the Arabic-first default.
    language: Optional[str] = Field(None, pattern="^(ar|en)$")
    terminology_mode: Optional[str] = Field(
        None, pattern="^(arabic_first|industry|english_technical)$"
    )


class AnswerChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None


class AnswerSubmissionResponse(BaseModel):
    id: int
    exercise_id: Optional[int]
    quiz_id: Optional[int]
    question_index: Optional[int]
    messages: List[AnswerChatMessage]
    is_correct: Optional[bool]
    score: Optional[float]
    updated_at: Optional[datetime]
    # Exercises only: an example answer exists and this learner may now see
    # it (after their first evaluated answer). None for quiz questions.
    example_available: Optional[bool] = None

    class Config:
        from_attributes = True


class ExampleAnswerResponse(BaseModel):
    example_answer: str
    example_answer_ar: Optional[str] = None
