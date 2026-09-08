"""
services/
  llm/          — LLM factory + providers (Anthropic, OpenAI)
  mentor/       — AI mentor chat
  code_review/  — AI code reviewer
  skill_gap/    — skill gap analyzer
  interview/    — mock interview questions
  roadmap/      — personalized roadmap generator
  utils.py      — shared JSON parsing helper

Usage in controllers:
    from app.services import get_llm, mentor_service
    llm = get_llm()
    reply, actions = mentor_service.get_mentor_reply(llm, history, message)
"""
from app.core.config import settings
from app.services.llm import LLMProviderFactory, LLMEnum, BaseLLMProvider

from app.services.mentor      import mentor_service       # noqa: F401
from app.services.mentor      import answer_evaluator_service  # noqa: F401
from app.services.code_review import code_review_service  # noqa: F401
from app.services.skill_gap   import skill_gap_service    # noqa: F401
from app.services.interview   import interview_service     # noqa: F401
from app.services.roadmap     import roadmap_service       # noqa: F401


def get_llm() -> BaseLLMProvider:
    """
    Return a configured LLM provider based on GENERATION_BACKEND setting.

    Supported values for GENERATION_BACKEND in .env:
        anthropic  →  requires ANTHROPIC_API_KEY
        openai     →  requires OPENAI_API_KEY
    """
    backend = settings.GENERATION_BACKEND

    # Give a clear error if the key is missing
    if backend == LLMEnum.ANTHROPIC.value and not settings.ANTHROPIC_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is missing from your .env file.\n"
            "Get a key at https://console.anthropic.com and add:\n"
            "  ANTHROPIC_API_KEY=sk-ant-..."
        )
    if backend == LLMEnum.OPENAI.value and not settings.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is missing from your .env file.\n"
            "Get a key at https://platform.openai.com and add:\n"
            "  OPENAI_API_KEY=sk-..."
        )

    factory = LLMProviderFactory(settings)
    provider = factory.create(backend)
    return provider


__all__ = [
    "get_llm",
    "mentor_service",
    "answer_evaluator_service",
    "code_review_service",
    "skill_gap_service",
    "interview_service",
    "roadmap_service",
]
