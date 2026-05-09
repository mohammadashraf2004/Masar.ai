"""
services/
  llm/                     — LLM factory + providers
  mentor/                  — AI mentor chat
  code_review/             — AI code reviewer
  skill_gap/               — skill gap analyzer
  interview/               — mock interview questions
  roadmap/                 — personalized roadmap generator
  utils.py                 — shared JSON parsing helper

Usage (in a controller):
    from app.services import get_llm, mentor_service

    llm = get_llm()
    reply, actions = mentor_service.get_mentor_reply(llm, history, message)
"""
from app.core.config import settings
from app.services.llm import LLMProviderFactory, BaseLLMProvider
from app.services.llm.providers.AnthropicProvider import AnthropicProvider
from app.services.llm.providers.OpenAIProvider import OpenAIProvider

from app.services.mentor import mentor_service
from app.services.code_review import code_review_service
from app.services.skill_gap import skill_gap_service
from app.services.interview import interview_service
from app.services.roadmap import roadmap_service


def get_llm() -> BaseLLMProvider:
    """Return a configured LLM provider based on GENERATION_BACKEND setting."""
    factory = LLMProviderFactory(settings)
    provider = factory.create(settings.GENERATION_BACKEND)
    if not provider.validate():
        raise RuntimeError(
            f"LLM provider '{settings.GENERATION_BACKEND}' is missing its API key. "
            "Check your .env file."
        )
    return provider


__all__ = [
    "get_llm",
    "mentor_service",
    "code_review_service",
    "skill_gap_service",
    "interview_service",
    "roadmap_service",
]
