"""Request/response schemas for Mentor v2 (/mentor/message, /mentor/quiz/answer).

JSON is camelCase on the wire (`lessonId`, `skillDelta`) to match the
frontend's v2 contract; snake_case names are accepted too.

Both request models set `extra="ignore"`, and that is load-bearing: the
client has no say over the learner's progress, mastery or grades. A
`progress`, `mastery` or `grades` key in the body is dropped here, before
any handler runs. Everything the mentor knows about the learner is read
from the database on the server.
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from app.views.mentor import MAX_MESSAGE_CHARS

Intent = Literal[
    "explain", "simplify", "example", "why", "hint",
    "socratic", "quiz", "practice", "review",
]
INTENTS: tuple = Intent.__args__  # type: ignore[attr-defined]

# Where a block's content came from, in retrieval order. "general" means
# general knowledge: nothing in the course backs it.
Grounding = Literal["lesson", "module", "prerequisite", "mistakes", "general"]

BlockKind = Literal["text", "code", "flow", "check", "hint", "quiz"]


class _Camel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="ignore")


class MentorV2Message(_Camel):
    # Optional only for a proactive trigger, which has no learner text.
    content: str = Field("", max_length=MAX_MESSAGE_CHARS)
    lesson_id: Optional[int] = Field(None, gt=0)
    exercise_id: Optional[int] = Field(None, gt=0)
    session_id: Optional[int] = Field(None, gt=0)
    # An explicit intent (a chip or a selection-toolbar button) always wins
    # over detection.
    intent: Optional[Intent] = None
    # Text the learner highlighted in the lesson ("explain this").
    selection: Optional[str] = Field(None, max_length=1_000)
    # Proactive, mentor-initiated turn. Always rule-based, never an LLM
    # call, so it is free and cannot be used to get free generation.
    trigger: Optional[Literal["lesson_completed"]] = None
    language: Optional[str] = Field(None, pattern="^(ar|en)$")
    terminology_mode: Optional[str] = Field(
        None, pattern="^(arabic_first|industry|english_technical)$"
    )

    @model_validator(mode="after")
    def _needs_text_or_trigger(self):
        if self.trigger is None and not self.content.strip() and not (self.selection or "").strip():
            raise ValueError("content is required")
        if self.trigger == "lesson_completed" and self.lesson_id is None:
            raise ValueError("lessonId is required for a lesson_completed trigger")
        return self


class BlockSource(_Camel):
    lesson_id: int
    title: str


class QuizQuestionOut(_Camel):
    """A quiz question as the learner sees it. There is no field for the
    correct option or the explanation, so neither can be serialized by
    accident."""
    quiz_id: int
    question_index: int
    question: str
    options: List[str]


class MentorBlock(_Camel):
    kind: BlockKind
    grounding: Grounding
    text: Optional[str] = None
    code: Optional[str] = None
    language: Optional[str] = None
    steps: Optional[List[str]] = None
    level: Optional[int] = None
    source: Optional[BlockSource] = None
    quiz: Optional[QuizQuestionOut] = None


class MentorContextOut(_Camel):
    lesson_id: Optional[int] = None
    lesson_title: Optional[str] = None
    module_title: Optional[str] = None
    exercise_id: Optional[int] = None
    exercise_title: Optional[str] = None


class MentorV2Response(_Camel):
    session_id: int
    intent: Intent
    # explicit | rules | model | default
    intent_source: str
    proactive: bool = False
    blocks: List[MentorBlock]
    credits_charged: int
    # True when validation failed twice and a rule-based reply was served.
    fallback: bool = False
    context: MentorContextOut


class QuizAnswerRequest(_Camel):
    quiz_id: int = Field(..., gt=0)
    question_index: int = Field(..., ge=0, le=500)
    choice: int = Field(..., ge=0, le=50)
    lesson_id: Optional[int] = Field(None, gt=0)
    language: Optional[str] = Field(None, pattern="^(ar|en)$")


class SkillDelta(_Camel):
    skill: str
    before: float  # confidence 0–1
    after: float
    status: str
    previous_status: str


class QuizAnswerResponse(_Camel):
    correct: bool
    feedback: List[MentorBlock]
    # Present only when the skill's confidence actually changed.
    skill_delta: Optional[SkillDelta] = None
