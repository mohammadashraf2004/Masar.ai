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
from app.services.llm import LLMProviderFactory, BaseLLMProvider

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
    # A clear error if the key is missing, the backend is misspelt or the
    # model id is blank. Names settings only — this text lands in the logs.
    # Callers turn it into a user-safe message; it is never shown to users.
    problems = settings.llm_config_problems()
    if problems:
        raise RuntimeError(
            "AI provider is not configured: " + "; ".join(problems)
            + ". Set them in backend/.env (local) or the deployment environment;"
            " see README.md, Environment variables."
        )

    factory = LLMProviderFactory(settings)
    provider = factory.create(settings.GENERATION_BACKEND)
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
