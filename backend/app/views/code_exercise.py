from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class CodePayload(BaseModel):
    code: str = Field(..., max_length=50_000)
    language: Literal["en", "ar"] = "en"


class FeedbackResponse(BaseModel):
    code: str
    message: str
    test_id: Optional[str] = None
    messages: dict[str, str] = Field(default_factory=dict)
    # True when the precise note was held back because it would quote part
    # of the answer; it is shown after the next different attempt.
    withheld: bool = False


class RunResponse(BaseModel):
    status: str
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: int


class AttemptStateResponse(BaseModel):
    failed_checks: int
    passed: bool
    completed_independently: bool
    solution_viewed: bool
    solution_available: bool
    checks_until_solution: int


class SubmitResponse(RunResponse):
    passed: bool
    feedback: FeedbackResponse
    tests_passed: int
    tests_total: int
    failed_test: Optional[str] = None
    # The learner's standing after this check (see attempt_state).
    attempt: Optional[AttemptStateResponse] = None


class CodeExerciseResponse(BaseModel):
    id: int
    title: str
    description: str
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    exercise_type: str
    language: Optional[str] = None
    starter_code: Optional[str] = None
    hint: Optional[str] = None
    hint_ar: Optional[str] = None
    grading_available: bool
    difficulty: Any
    skill_tested: list[str]

    class Config:
        from_attributes = True


class SolutionResponse(BaseModel):
    solution_code: str
