"""Request and response shapes of the Mentor v2 endpoints.

They mirror the frontend contract (frontend/src/features/mentor/types.ts), so the names are
camelCase. What the client may send is deliberately small: ids, an intent, the text it
selected and what the learner typed. There is no field for progress, mastery, grades or a
quiz answer - the server works those out itself, and an unknown field is ignored.
"""
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

MAX_TEXT_CHARS = 2_000
MAX_SELECTED_CHARS = 1_200
# The learner's own exercise draft. It is their text, not course content: it is sent to the
# model as the learner's code and never trusted as an instruction or a source.
MAX_CODE_CHARS = 8_000

INTENTS = (
    "EXPLAIN", "SIMPLIFY", "HINT", "SOCRATIC", "DEBUG", "QUIZ", "PRACTICE",
    "REVIEW", "CONNECT", "WHY", "PROJECT_COACH", "CAREER_CONTEXT", "GENERAL_QUESTION",
)
CONTEXT_ONLY_INTENTS = {"HINT", "QUIZ", "REVIEW"}
Intent = Literal[
    "EXPLAIN", "SIMPLIFY", "HINT", "SOCRATIC", "DEBUG", "QUIZ", "PRACTICE",
    "REVIEW", "CONNECT", "WHY", "PROJECT_COACH", "CAREER_CONTEXT", "GENERAL_QUESTION",
]

# What a server-verified proactive message can be about. The client names the trigger; the
# server checks it against the learner's own progress before it says anything.
Trigger = Literal["lesson_completed"]


class MentorContextIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    courseId: Optional[str] = Field(None, max_length=120)
    lessonId: Optional[str] = Field(None, pattern=r"^\d{1,9}$")
    exerciseId: Optional[str] = Field(None, pattern=r"^\d{1,9}$")
    attachCode: Optional[bool] = None
    selectedText: Optional[str] = Field(None, max_length=MAX_SELECTED_CHARS)
    # What is in the exercise editor now. Only read with an exerciseId and attachCode.
    code: Optional[str] = Field(None, max_length=MAX_CODE_CHARS)


class MentorMessageIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    text: Optional[str] = Field(None, min_length=1, max_length=MAX_TEXT_CHARS)
    intent: Optional[Intent] = None
    trigger: Optional[Trigger] = None
    context: MentorContextIn = Field(default_factory=MentorContextIn)
    # The learner's own language settings; they only ever select prompt text.
    language: Optional[str] = Field(None, pattern="^(ar|en)$")
    terminology_mode: Optional[str] = Field(None, pattern="^(arabic_first|industry|english_technical)$")
    # Client-made id of this send. A retry of the same send (after a timeout the server may
    # have survived) carries the same id and gets the stored reply back, never a second charge.
    requestId: Optional[str] = Field(None, pattern=r"^[A-Za-z0-9_-]{8,64}$")
    # The learner started a new conversation: earlier turns of this scope are not history.
    fresh: Optional[bool] = None
    # For HINT: how strong a hint (1 a nudge, 2 a direction, 3 detailed guidance). The full
    # solution is never a mentor reply; the exercise's own "show solution" owns that.
    hintLevel: Optional[int] = Field(None, ge=1, le=3)

    @model_validator(mode="after")
    def _text_or_trigger(self):
        has_text = bool(self.text and self.text.strip())
        uses_visible_context = self.intent in CONTEXT_ONLY_INTENTS
        if not has_text and not self.trigger and not uses_visible_context:
            raise ValueError(
                "a message needs text, a context-only intent, or a trigger the server can verify"
            )
        return self


class ProactiveOut(BaseModel):
    trigger: str


class MentorMessageOut(BaseModel):
    id: str
    role: Literal["mentor"] = "mentor"
    intent: Optional[str] = None
    proactive: Optional[ProactiveOut] = None
    blocks: List[Dict[str, Any]]
    # What this reply cost. 0 for a rule-based or proactive reply, and for one that fell back
    # because the model's answer did not pass validation (the charge is returned).
    creditCost: int
    sessionId: int
    # True when this is the stored reply to a send already answered (same requestId). Its
    # creditCost is what that send cost - charged once, by the original, never again.
    replayed: bool = False


class QuizAnswerIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    quizId: str = Field(..., pattern=r"^\d{1,9}:\d{1,4}$")
    optionId: str = Field(..., pattern=r"^[a-h]$")
    language: Optional[str] = Field(None, pattern="^(ar|en)$")


class SkillDeltaOut(BaseModel):
    skill: str
    # 0-100 confidence before and after this answer.
    from_: int = Field(..., alias="from")
    to: int
    status: Literal["learning", "needs_review", "mastered"]

    model_config = ConfigDict(populate_by_name=True)


class QuizAnswerOut(BaseModel):
    correct: bool
    feedback: List[Dict[str, Any]]
    skillDelta: Optional[SkillDeltaOut] = None


class MentorContextOut(BaseModel):
    """Where the learner is, so the hub can attach it without guessing."""
    courseId: Optional[str] = None
    lessonId: Optional[str] = None
    exerciseId: Optional[str] = None
    courseTitle: Optional[str] = None
    lessonTitle: Optional[str] = None
    exerciseTitle: Optional[str] = None
    lessonNumber: Optional[int] = None
    lessonTotal: Optional[int] = None
    # Whether the learner is enrolled in this course: only such a course can be chosen in the
    # hub as what a conversation is about.
    courseEnrolled: Optional[bool] = None


class MentorCourseOut(BaseModel):
    courseId: str
    title: str
    lessonsDone: int
    lessonsTotal: int


class MentorCoursesOut(BaseModel):
    """The courses the learner is enrolled in, for the hub's course picker."""
    courses: List[MentorCourseOut]
