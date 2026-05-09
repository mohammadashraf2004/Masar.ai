from typing import List

from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are an expert curriculum designer for tech careers.
Generate a personalized weekly learning roadmap.

Return ONLY a valid JSON array of weeks:
[
  {
    "week": 1,
    "theme": "...",
    "topics": ["topic1", "topic2"],
    "project": "mini project description",
    "goal": "what the student will be able to do by end of week"
  }
]
Generate exactly 4 weeks."""


def generate_roadmap(
    llm: BaseLLMProvider,
    track: str,
    experience_level: str,
    weak_skills: List[str] = None,
    completed_topics: List[str] = None,
) -> List[dict]:
    weak_skills = weak_skills or []
    completed_topics = completed_topics or []

    message = (
        f"Track: {track}\n"
        f"Experience level: {experience_level}\n"
        f"Weak areas: {', '.join(weak_skills) if weak_skills else 'none identified yet'}\n"
        f"Already covered: {', '.join(completed_topics) if completed_topics else 'just starting'}"
    )

    raw = llm.chat(system=SYSTEM_PROMPT, messages=[{"role": "user", "content": message}], max_tokens=1000)
    result = parse_json_response(raw, [])
    return result if isinstance(result, list) else []
